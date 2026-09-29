from src.constants.device_type import DeviceType
from src.constants.log_templates import LOG_TEMPLATES
from src.repositories.checklist_version_repository import ChecklistVersionRepository
from src.repositories.store import store
from src.utils.domain_error import DomainError

# 建任务请求未带版本号时的并发判定窗口（秒）：发布与建任务几乎同时发生
CONCURRENT_PUBLISH_WINDOW_SECONDS = 30


class ChecklistVersionService:
    def __init__(self):
        self.repo = ChecklistVersionRepository()

    def list_versions(self, task_type: str | None = None):
        rows = self.repo.find_all()
        if task_type:
            rows = [row for row in rows if row["task_type"] == task_type]
        return rows

    def get_current(self, task_type: str):
        version = self.repo.find_published(task_type)
        if version is None:
            raise DomainError("CHECKLIST_NOT_FOUND")
        return version

    def create_draft(self, payload: dict, actor=1):
        task_type = payload.get("task_type")
        items = payload.get("items") or []
        if task_type not in DeviceType:
            raise DomainError("VALIDATION_FAILED", f"unsupported task_type: {task_type}")
        if not items:
            raise DomainError("VALIDATION_FAILED", "checklist items must not be empty")
        self._validate_items(items, task_type)
        draft = self.repo.create_draft(
            task_type, items, payload.get("remark", ""), actor, payload.get("scope_key", "DEFAULT")
        )
        store.append_log(
            actor, LOG_TEMPLATES["ChecklistVersion"][0], "ChecklistVersion", draft["id"],
            f"task_type={task_type} version=v{draft['version']} items={len(items)}",
        )
        return draft

    def publish(self, version_id, actor=1):
        version = self.repo.find_by_id(version_id)
        if version is None:
            raise DomainError("CHECKLIST_NOT_FOUND")
        if version["status"] == "PUBLISHED":
            raise DomainError("CHECKLIST_ALREADY_PUBLISHED")
        published = self.repo.publish(version_id, actor)
        # 发布动作可追溯：旧任务继续引用旧版本快照，仅新任务取新版本
        store.append_log(
            actor, LOG_TEMPLATES["ChecklistVersion"][1], "ChecklistVersion", version_id,
            f"task_type={published['task_type']} version=v{published['version']} published",
        )
        return published

    def resolve_for_task_creation(self, payload: dict) -> tuple[dict, str]:
        """建任务时确定清单版本，返回 (已发布版本, 给创建人的提示)。

        - expected_version_id 与当前发布不一致：说明填表期间发生了发布，采用新版本并提示；
        - 未带 expected_version_id 且发布就发生在并发窗口内：同样提示创建人。
        """
        task_type = payload.get("task_type")
        current = self.repo.find_published(task_type)
        if current is None:
            raise DomainError("CHECKLIST_NOT_PUBLISHED", f"no published checklist for {task_type}")
        notice = ""
        expected_id = payload.get("expected_version_id")
        if expected_id is not None and int(expected_id) != int(current["id"]):
            notice = (
                f"清单在创建期间已发布新版本 v{current['version']}，"
                f"任务已自动采用最新已发布版本。"
            )
            store.append_log(
                payload.get("created_by", 1),
                LOG_TEMPLATES["ChecklistVersion"][2],
                "ChecklistVersion", current["id"],
                f"concurrent publish detected by task create, pinned=v{current['version']}",
            )
        elif expected_id is None and self._published_within_window(current):
            notice = (
                f"清单 v{current['version']} 刚刚发布，本次任务已采用该已发布版本，"
                f"执行期间不再受后续改版影响。"
            )
        return current, notice

    def _published_within_window(self, version: dict) -> bool:
        from datetime import datetime, timezone

        published_at = version.get("published_at")
        if not published_at:
            return False
        try:
            published_ts = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return False
        delta = (datetime.now(timezone.utc) - published_ts).total_seconds()
        return 0 <= delta <= CONCURRENT_PUBLISH_WINDOW_SECONDS

    def _validate_items(self, items: list, task_type: str):
        codes = set()
        for item in items:
            code = item.get("item_code")
            if not code or code in codes:
                raise DomainError("VALIDATION_FAILED", f"duplicate or empty item_code: {code}")
            codes.add(code)
            if item.get("device_type", task_type) != task_type:
                raise DomainError("VALIDATION_FAILED", f"item {code} device_type mismatch")
            if item.get("rule_type") not in ("NUMERIC", "CHOICE", "TEXT"):
                raise DomainError("VALIDATION_FAILED", f"item {code} invalid rule_type")
            if item.get("severity") not in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
                raise DomainError("VALIDATION_FAILED", f"item {code} invalid severity")
