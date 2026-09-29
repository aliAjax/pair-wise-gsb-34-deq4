from src.constants.log_templates import LOG_TEMPLATES
from src.repositories.hazard_ticket_repository import HazardTicketRepository
from src.repositories.inspection_result_repository import InspectionResultRepository
from src.repositories.inspection_task_repository import InspectionTaskRepository
from src.repositories.store import store
from src.services.checklist_version_service import ChecklistVersionService
from src.utils.checklist_grader import ChecklistGrader
from src.utils.domain_error import DomainError
from src.utils.formatters import checklist_version_label


class InspectionTaskService:
    def __init__(self):
        self.repo = InspectionTaskRepository()
        self.result_repo = InspectionResultRepository()
        self.hazard_repo = HazardTicketRepository()
        self.checklist_service = ChecklistVersionService()

    def list(self):
        return self.repo.find_all()

    def get(self, task_id):
        task = self.repo.find_by_id(task_id)
        if task is None:
            raise DomainError("TASK_NOT_FOUND")
        task["results"] = self.result_repo.find_by_task(task_id)
        return task

    def create(self, payload: dict, actor=1):
        # 与发布共用 store 锁：发布与建任务同时发生时被串行化，
        # 任务取锁内读到的"当前已发布版本"，并向创建人返回版本提示。
        payload = dict(payload)
        payload["created_by"] = actor
        with store.lock:
            version, notice = self.checklist_service.resolve_for_task_creation(payload)
            task_payload = {
                "building_id": payload.get("building_id"),
                "inspector_id": payload.get("inspector_id", actor),
                "plan_date": payload.get("plan_date", ""),
                "task_type": version["task_type"],
                "checklist_version": checklist_version_label(version["version"]),
                "checklist_version_id": version["id"],
                "version_no": version["version"],
                # 检查项与判级规则整体快照，后续发布不再影响该任务
                "pinned_items": version["items"],
                "created_by": actor,
                "version_notice": notice,
            }
            if not task_payload["building_id"]:
                raise DomainError("VALIDATION_FAILED", "building_id is required")
            task = self.repo.create(task_payload)
            store.append_log(
                actor, LOG_TEMPLATES["InspectionTask"][4], "InspectionTask", task["id"],
                f"pinned checklist {task['task_type']} v{version['version']} "
                f"version_id={version['id']} notice={'yes' if notice else 'no'}",
            )
        return task

    def submit(self, task_id, payload: dict, actor=1):
        entries = payload.get("entries") or []
        with store.lock:
            task = self.repo.find_by_id(task_id)
            if task is None:
                raise DomainError("TASK_NOT_FOUND")
            if task["status"] in ("SUBMITTED", "REVIEWED"):
                raise DomainError("TASK_ALREADY_SUBMITTED")

            pinned = {item["item_code"]: item for item in task.get("pinned_items", [])}
            version_label = task.get("checklist_version", "")
            result_rows = []
            abnormal = []
            for entry in entries:
                item_code = entry.get("item_code")
                if item_code not in pinned:
                    # 提交项不属于建任务时固定的版本，拒绝按新版本判级
                    raise DomainError("CHECKLIST_ITEM_NOT_FOUND", f"item {item_code} not in {version_label}")
                grade = ChecklistGrader.grade(pinned[item_code], entry.get("measured_value", ""))
                result_rows.append({
                    "task_id": task["id"],
                    "device_id": entry.get("device_id"),
                    "item_code": item_code,
                    "result_status": grade["result_status"],
                    "judged_severity": grade["judged_severity"],
                    "checklist_version": version_label,
                    "measured_value": entry.get("measured_value", ""),
                    "photo_url": entry.get("photo_url", ""),
                    "note": entry.get("note", ""),
                })
                if grade["result_status"] == "ABNORMAL":
                    abnormal.append((result_rows[-1], grade["judged_severity"]))

            results = self.result_repo.bulk_create(result_rows)
            created_tickets, merged_tickets = self._raise_or_merge_hazards(results, abnormal, actor)
            self.repo.mark_submitted(task_id)
            store.append_log(
                actor, LOG_TEMPLATES["InspectionTask"][5], "InspectionTask", task_id,
                f"submitted by {version_label}: {len(results)} results, "
                f"{len(abnormal)} abnormal, {len(created_tickets)} new tickets, "
                f"{len(merged_tickets)} merged",
            )
        return {
            "task": self.repo.find_by_id(task_id),
            "results": results,
            "abnormal_count": len(abnormal),
            "created_tickets": created_tickets,
            "merged_tickets": merged_tickets,
        }

    def _raise_or_merge_hazards(self, results: list, abnormal: list, actor):
        """异常项生成隐患单；同一设备已有未关闭隐患则合并并累计发现次数。"""
        result_by_key = {r["item_code"]: r for r in results}
        created, merged = [], []
        for abnormal_result, severity in abnormal:
            result = result_by_key[abnormal_result["item_code"]]
            device_id = result["device_id"]
            existing = self.hazard_repo.find_open_by_device(device_id)
            if existing is not None:
                ticket = self.hazard_repo.merge_find(existing["id"], result["id"], severity)
                store.append_log(
                    actor, LOG_TEMPLATES["HazardTicket"][4], "HazardTicket", ticket["id"],
                    f"merged result={result['id']} device={device_id} "
                    f"found_count={ticket['found_count']} severity={ticket['severity']}",
                )
                merged.append(ticket)
            else:
                ticket = self.hazard_repo.create({
                    "result_id": result["id"],
                    "device_id": device_id,
                    "severity": severity,
                })
                store.append_log(
                    actor, LOG_TEMPLATES["HazardTicket"][0], "HazardTicket", ticket["id"],
                    f"created from result={result['id']} device={device_id} severity={severity}",
                )
                created.append(ticket)
        return created, merged
