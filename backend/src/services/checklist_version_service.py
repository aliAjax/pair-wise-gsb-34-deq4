from __future__ import annotations
import copy

from src.constants.checklist_status import CHECKLIST_PUBLISHED, CHECKLIST_ARCHIVED
from src.constants.error_codes import (
    CHECKLIST_NOT_FOUND,
    CHECKLIST_NOT_PUBLISHABLE,
    CHECKLIST_NO_PUBLISHED_VERSION,
    CHECKLIST_ITEM_CODE_CONFLICT,
    VALIDATION_FAILED,
)
from src.constants.error_messages import ERROR_MESSAGES
from src.exceptions.service_error import ServiceError
from src.repositories.checklist_version_repository import ChecklistVersionRepository
from src.constructors.checklist_version_factory import create_checklist_version_dto
from src.utils.clock import utc_now_iso
from src.utils.audit import record_audit
from src.utils.locks import named_lock


class ChecklistVersionService:
    def __init__(self):
        self.repo = ChecklistVersionRepository()

    def list(self):
        return self.repo.find_all()

    def get(self, version_id: int):
        row = self.repo.find_by_id(version_id)
        if row is None:
            raise ServiceError(
                CHECKLIST_NOT_FOUND,
                ERROR_MESSAGES[CHECKLIST_NOT_FOUND].format(checklist_id=version_id),
                http_status=404,
            )
        return row

    def _validate_items(self, version: str, items: list[dict]):
        if not items:
            raise ServiceError(
                VALIDATION_FAILED,
                ERROR_MESSAGES[VALIDATION_FAILED],
                http_status=422,
            )
        codes = [item["item_code"] for item in items]
        duplicated = {code for code in codes if codes.count(code) > 1}
        if duplicated:
            code = next(iter(duplicated))
            raise ServiceError(
                CHECKLIST_ITEM_CODE_CONFLICT,
                ERROR_MESSAGES[CHECKLIST_ITEM_CODE_CONFLICT].format(item_code=code, version=version),
                http_status=422,
            )

    def create_draft(self, payload) -> dict:
        """物业起草新清单版本。草稿不影响任何已领取任务。"""
        data = payload.model_dump() if hasattr(payload, "model_dump") else dict(payload)
        items = data.get("items") or []
        self._validate_items(data["version"], items)
        if self.repo.find_draft_by_type_and_version(data["task_type"], data["version"]) is not None:
            raise ServiceError(
                CHECKLIST_ITEM_CODE_CONFLICT,
                f"version {data['version']} already exists for task_type {data['task_type']}",
                http_status=409,
            )
        now = utc_now_iso()
        row = create_checklist_version_dto(
            id=self._next_id(),
            task_type=data["task_type"],
            version=data["version"],
            status="DRAFT",
            remark=data.get("remark", ""),
            created_by=data.get("created_by", 1),
            created_at=now,
            items=copy.deepcopy(items),
        )
        saved = self.repo.create(row)
        record_audit(
            data.get("created_by", 1),
            "ChecklistVersion.create",
            "ChecklistVersion",
            saved["id"],
            {"task_type": saved["task_type"], "version": saved["version"], "items": len(saved["items"])},
            created_at=now,
        )
        return saved

    def publish(self, version_id: int, actor_id: int = 1, published_at: str | None = None) -> dict:
        """发布草稿：同任务类型的旧已发布版本归档，新版本成为建任务唯一固定口径。"""
        row = self.repo.find_by_id(version_id)
        if row is None:
            raise ServiceError(
                CHECKLIST_NOT_FOUND,
                ERROR_MESSAGES[CHECKLIST_NOT_FOUND].format(checklist_id=version_id),
                http_status=404,
            )
        if row["status"] != "DRAFT":
            raise ServiceError(
                CHECKLIST_NOT_PUBLISHABLE,
                ERROR_MESSAGES[CHECKLIST_NOT_PUBLISHABLE].format(status=row["status"]),
                http_status=409,
            )
        self._validate_items(row["version"], row["items"])

        # 与建任务互斥：发布和建任务同时发生时，二者串行，新任务一定采用已发布版本
        with named_lock(f"checklist:{row['task_type']}"):
            moment = published_at or utc_now_iso()
            archived = []
            for older in self.repo.find_published_by_type(row["task_type"]):
                older["status"] = CHECKLIST_ARCHIVED
                older["archived_at"] = moment
                self.repo.update(older)
                archived.append(older["version"])
                record_audit(
                    actor_id,
                    "ChecklistVersion.archive",
                    "ChecklistVersion",
                    older["id"],
                    {"task_type": older["task_type"], "version": older["version"],
                     "replaced_by": row["version"]},
                    created_at=moment,
                )

            row["status"] = CHECKLIST_PUBLISHED
            row["published_by"] = actor_id
            row["published_at"] = moment
            saved = self.repo.update(row)

        record_audit(
            actor_id,
            "ChecklistVersion.publish",
            "ChecklistVersion",
            saved["id"],
            {"task_type": saved["task_type"], "version": saved["version"],
             "items": len(saved["items"]), "archived_versions": archived},
            created_at=moment,
        )
        return saved

    def latest_published(self, task_type: str):
        row = self.repo.find_latest_published(task_type)
        if row is None:
            raise ServiceError(
                CHECKLIST_NO_PUBLISHED_VERSION,
                ERROR_MESSAGES[CHECKLIST_NO_PUBLISHED_VERSION].format(task_type=task_type),
                http_status=409,
            )
        return row

    def _next_id(self) -> int:
        return max([r["id"] for r in self.repo.find_all()] or [0]) + 1
