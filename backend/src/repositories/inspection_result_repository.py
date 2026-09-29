import copy

from src.repositories.store import now_iso, store


class InspectionResultRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.inspection_result)

    def find_by_task(self, task_id):
        with store.lock:
            return [copy.deepcopy(row) for row in store.inspection_result if row["task_id"] == task_id]

    def bulk_create(self, rows: list):
        created = []
        with store.lock:
            for payload in rows:
                row = dict(payload)
                row["id"] = store.next_id("inspection_result")
                row.setdefault("photo_url", "")
                row.setdefault("note", "")
                row.setdefault("submitted_at", now_iso())
                store.inspection_result.append(row)
                created.append(copy.deepcopy(row))
        return created
