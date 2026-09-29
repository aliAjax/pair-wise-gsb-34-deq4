from __future__ import annotations
import copy

from src.constants.error_codes import (
    TASK_NOT_FOUND,
    TASK_NOT_SUBMITTABLE,
    TASK_CHECKLIST_VERSION_MISSING,
    RESULT_ITEM_UNKNOWN,
)
from src.constants.error_messages import ERROR_MESSAGES
from src.constants.inspection_status import (
    TASK_STATUS_SUBMITTED,
    TASK_SUBMITTABLE_STATUSES,
)
from src.constants.result_outcome import (
    RESULT_OUTCOME_ABNORMAL,
    RESULT_OUTCOME_NOT_CHECKED,
)
from src.exceptions.service_error import ServiceError
from src.repositories.inspection_task_repository import InspectionTaskRepository
from src.repositories.inspection_result_repository import InspectionResultRepository
from src.repositories.fire_device_repository import FireDeviceRepository
from src.services.checklist_version_service import ChecklistVersionService
from src.services.hazard_ticket_service import HazardTicketService
from src.constructors.inspection_task_factory import create_inspection_task_dto
from src.utils.clock import utc_now_iso
from src.utils.audit import record_audit
from src.utils.locks import named_lock
from src.utils.checklist_grader import grade_item, severity_for_outcome

# 发布与建任务在该时间窗（毫秒）内发生即视为“同时发生”，需提示创建人
SIMULTANEOUS_WINDOW_MS = 1000


def _parse_ts(value: str):
    from datetime import datetime
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _is_simultaneous(published_at: str | None, created_at: str) -> bool:
    """发布时间与建任务时间相差不超过 SIMULTANEOUS_WINDOW_MS 即视为同时发生。"""
    if not published_at:
        return False
    delta_ms = abs((_parse_ts(created_at) - _parse_ts(published_at)).total_seconds()) * 1000
    return delta_ms <= SIMULTANEOUS_WINDOW_MS


class InspectionTaskService:
    def __init__(self):
        self.repo = InspectionTaskRepository()
        self.result_repo = InspectionResultRepository()
        self.device_repo = FireDeviceRepository()
        self.checklist_service = ChecklistVersionService()
        self.hazard_service = HazardTicketService()

    def list(self):
        return self.repo.find_all()

    def get(self, task_id: int):
        row = self.repo.find_by_id(task_id)
        if row is None:
            raise ServiceError(
                TASK_NOT_FOUND,
                ERROR_MESSAGES[TASK_NOT_FOUND].format(task_id=task_id),
                http_status=404,
            )
        return row

    def create(self, payload, created_at: str | None = None) -> dict:
        """建任务：在锁内取“当前最新已发布版本”并固定到任务上。

        随后该版本即使被归档/替换，任务仍保留固定版本号与检查项快照，
        执行与提交都不受后续发布影响。
        """
        data = payload.model_dump() if hasattr(payload, "model_dump") else dict(payload)
        task_type = data["task_type"]
        now = created_at or utc_now_iso()
        with named_lock(f"checklist:{task_type}"):
            pinned = self.checklist_service.latest_published(task_type)
            max_id = max([row["id"] for row in self.repo.find_all()] or [0])
            # 与建任务“同时”发生的发布：新任务采用该已发布版本并提示创建人
            simultaneous = _is_simultaneous(pinned["published_at"], now)
            notice = (
                f"清单 {task_type} 于建任务同时发布了新版本 {pinned['version']}，"
                f"本任务已固定采用该已发布版本。"
                if simultaneous else ""
            )
            row = create_inspection_task_dto(
                id=max_id + 1,
                building_id=data["building_id"],
                inspector_id=data["inspector_id"],
                plan_date=data["plan_date"],
                task_type=task_type,
                status="PLANNED",
                checklist_version=pinned["version"],
                checklist_version_id=pinned["id"],
                version_pinned_at=now,
                created_by=data.get("created_by", 1),
                version_notice=notice,
                finished_at="",
                checklist_snapshot=copy.deepcopy(pinned["items"]),
            )
            saved = self.repo.create(row)

        record_audit(
            data.get("created_by", 1),
            "InspectionTask.pin_checklist",
            "InspectionTask",
            saved["id"],
            {"task_type": task_type, "pinned_version": pinned["version"],
             "checklist_version_id": pinned["id"], "simultaneous_publish": simultaneous},
            created_at=now,
        )
        return saved

    def submit(self, task_id: int, payload, submitted_at: str | None = None) -> dict:
        """按任务固定版本判级提交。

        - 检查项以任务快照为准，后续发布的新检查项不会混进来
        - 检查项不在固定版本内则拒绝，防止按新规则误判
        - 异常项生成隐患单，同设备未关闭隐患合并并累计发现次数
        """
        task = self.repo.find_by_id(task_id)
        if task is None:
            raise ServiceError(
                TASK_NOT_FOUND,
                ERROR_MESSAGES[TASK_NOT_FOUND].format(task_id=task_id),
                http_status=404,
            )
        if task["status"] not in TASK_SUBMITTABLE_STATUSES:
            raise ServiceError(
                TASK_NOT_SUBMITTABLE,
                ERROR_MESSAGES[TASK_NOT_SUBMITTABLE].format(task_id=task_id, status=task["status"]),
                http_status=409,
            )
        snapshot = task.get("checklist_snapshot")
        if not snapshot:
            raise ServiceError(
                TASK_CHECKLIST_VERSION_MISSING,
                ERROR_MESSAGES[TASK_CHECKLIST_VERSION_MISSING].format(task_id=task_id),
                http_status=409,
            )

        items_by_code = {item["item_code"]: item for item in snapshot}
        inputs = payload.model_dump()["results"] if hasattr(payload, "model_dump") else payload["results"]
        input_codes = [row["item_code"] for row in inputs]
        unknown = [code for code in input_codes if code not in items_by_code]
        if unknown:
            raise ServiceError(
                RESULT_ITEM_UNKNOWN,
                ERROR_MESSAGES[RESULT_ITEM_UNKNOWN].format(
                    item_code=unknown[0], version=task["checklist_version"], task_id=task_id),
                http_status=422,
            )

        now = submitted_at or utc_now_iso()
        actor_id = payload.model_dump().get("actor_id", 1) if hasattr(payload, "model_dump") else 1
        graded_results = []
        created_hazards = []
        merged_hazard_ids = []

        # 快照中存在但本次未录入的检查项标记为 NOT_CHECKED，既不会“被换掉”，也不会凭空判异常
        input_by_code = {row["item_code"]: row for row in inputs}
        next_result_id = max([r["id"] for r in self.result_repo.find_all()] or [0])
        for code, item in items_by_code.items():
            entry = input_by_code.get(code)
            if entry is None:
                outcome = RESULT_OUTCOME_NOT_CHECKED
                measured_value = ""
                result_status = RESULT_OUTCOME_NOT_CHECKED
                note = "固定版本检查项未录入"
                photo_url = ""
                device_id = None
            else:
                measured_value = entry.get("measured_value", "")
                outcome = grade_item(item, measured_value)
                result_status = entry.get("result_status", "DONE")
                note = entry.get("note", "")
                photo_url = entry.get("photo_url", "")
                device_id = entry.get("device_id")

            next_result_id += 1
            result_row = {
                "id": next_result_id,
                "task_id": task_id,
                "device_id": device_id,
                "item_code": code,
                "result_status": result_status,
                "measured_value": measured_value,
                "photo_url": photo_url,
                "note": note,
                "outcome": outcome,
                "checklist_version": task["checklist_version"],
                "graded_at": now,
            }
            saved_result = self.result_repo.create(result_row)
            graded_results.append(saved_result)
            record_audit(
                actor_id,
                "InspectionResult.grade",
                "InspectionResult",
                saved_result["id"],
                {"task_id": task_id, "item_code": code, "version": task["checklist_version"],
                 "outcome": outcome, "measured_value": measured_value},
                created_at=now,
            )

            if outcome == RESULT_OUTCOME_ABNORMAL:
                severity = severity_for_outcome(item, outcome)
                hazard = self.hazard_service.raise_for_abnormal_result(
                    saved_result, device_id, severity, actor_id=actor_id, moment=now)
                if hazard["found_count"] > 1:
                    merged_hazard_ids.append(hazard["id"])
                created_hazards.append(hazard)

        task["status"] = TASK_STATUS_SUBMITTED
        task["finished_at"] = now
        self.repo.update(task)
        record_audit(
            actor_id,
            "InspectionTask.submit",
            "InspectionTask",
            task_id,
            {"version": task["checklist_version"], "graded": len(graded_results),
             "abnormal": sum(1 for r in graded_results if r["outcome"] == RESULT_OUTCOME_ABNORMAL),
             "hazard_tickets": [h["id"] for h in created_hazards],
             "merged_hazard_ids": merged_hazard_ids},
            created_at=now,
        )

        return {
            "task": task,
            "results": graded_results,
            "hazard_tickets": created_hazards,
            "merged_hazard_ids": merged_hazard_ids,
        }
