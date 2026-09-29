from src.repositories import store


class ChecklistVersionRepository:
    def _rows(self):
        return store.get_store()["checklistVersion"]

    def find_all(self):
        with store.lock():
            return [dict(row) for row in self._rows()]

    def find_by_id(self, version_id: int):
        with store.lock():
            for row in self._rows():
                if row["id"] == version_id:
                    return dict(row)
        return None

    def find_draft_by_type_and_version(self, task_type: str, version: str):
        with store.lock():
            for row in self._rows():
                if row["task_type"] == task_type and row["version"] == version:
                    return dict(row)
        return None

    def find_published_by_type(self, task_type: str):
        """返回某任务类型当前所有已发布版本（按发布时间升序）。"""
        with store.lock():
            rows = [
                dict(row) for row in self._rows()
                if row["task_type"] == task_type and row["status"] == "PUBLISHED"
            ]
        return sorted(rows, key=lambda r: r["published_at"] or "")

    def find_latest_published(self, task_type: str):
        rows = self.find_published_by_type(task_type)
        return rows[-1] if rows else None

    def create(self, row: dict):
        with store.lock():
            self._rows().append(row)
            return dict(row)

    def update(self, row: dict):
        with store.lock():
            for index, current in enumerate(self._rows()):
                if current["id"] == row["id"]:
                    self._rows()[index] = row
                    return dict(row)
        return None
