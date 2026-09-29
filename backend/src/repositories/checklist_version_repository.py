import copy

from src.repositories.store import now_iso, store


class ChecklistVersionRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.checklist_version)

    def find_by_id(self, version_id):
        with store.lock:
            for row in store.checklist_version:
                if row["id"] == version_id:
                    return copy.deepcopy(row)
        return None

    def find_drafts_by_task_type(self, task_type: str, scope_key: str = "DEFAULT"):
        with store.lock:
            return [
                copy.deepcopy(row)
                for row in store.checklist_version
                if row["task_type"] == task_type
                and row["scope_key"] == scope_key
                and row["status"] == "DRAFT"
            ]

    def find_published(self, task_type: str, scope_key: str = "DEFAULT"):
        """返回该类型当前已发布版本；发布后旧版本行保留，按 version 取最大。"""
        with store.lock:
            matched = [
                row
                for row in store.checklist_version
                if row["task_type"] == task_type
                and row["scope_key"] == scope_key
                and row["status"] == "PUBLISHED"
            ]
        if not matched:
            return None
        return copy.deepcopy(max(matched, key=lambda r: r["version"]))

    def next_version_no(self, task_type: str, scope_key: str = "DEFAULT") -> int:
        with store.lock:
            current = [
                row["version"]
                for row in store.checklist_version
                if row["task_type"] == task_type and row["scope_key"] == scope_key
            ]
        return (max(current) + 1) if current else 1

    def create_draft(self, task_type: str, items: list, remark: str, actor, scope_key: str = "DEFAULT"):
        with store.lock:
            row = {
                "id": store.next_id("checklist_version"),
                "task_type": task_type,
                "scope_key": scope_key,
                "version": self.next_version_no(task_type, scope_key),
                "status": "DRAFT",
                "items": copy.deepcopy(items),
                "published_at": "",
                "published_by": None,
                "created_at": now_iso(),
                "created_by": actor,
                "remark": remark,
            }
            store.checklist_version.append(row)
            return copy.deepcopy(row)

    def publish(self, version_id, actor) -> dict | None:
        """发布为不可变版本：发布后的版本行永不被再次修改，新任务只能引用新版本。"""
        with store.lock:
            for row in store.checklist_version:
                if row["id"] == version_id:
                    if row["status"] == "PUBLISHED":
                        return copy.deepcopy(row)
                    row["status"] = "PUBLISHED"
                    row["published_at"] = now_iso()
                    row["published_by"] = actor
                    return copy.deepcopy(row)
        return None
