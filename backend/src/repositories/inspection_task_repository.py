import copy

from src.repositories.store import now_iso, store


class InspectionTaskRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.inspection_task)

    def find_by_id(self, task_id):
        with store.lock:
            for row in store.inspection_task:
                if row["id"] == task_id:
                    return copy.deepcopy(row)
        return None

    def create(self, payload: dict) -> dict:
        with store.lock:
            row = {
                "id": store.next_id("inspection_task"),
                "building_id": payload["building_id"],
                "inspector_id": payload["inspector_id"],
                "plan_date": payload.get("plan_date", now_iso()),
                "task_type": payload["task_type"],
                "status": "PLANNED",
                # 建任务时固定当时的已发布版本
                "checklist_version": payload["checklist_version"],
                "checklist_version_id": payload["checklist_version_id"],
                "version_no": payload["version_no"],
                "pinned_items": copy.deepcopy(payload["pinned_items"]),
                "finished_at": "",
                "created_at": now_iso(),
                "created_by": payload.get("created_by"),
                "version_notice": payload.get("version_notice", "")
            }
            store.inspection_task.append(row)
            return copy.deepcopy(row)

    def mark_submitted(self, task_id: int) -> dict | None:
        with store.lock:
            for row in store.inspection_task:
                if row["id"] == task_id:
                    row["status"] = "SUBMITTED"
                    row["finished_at"] = now_iso()
                    return copy.deepcopy(row)
        return None
