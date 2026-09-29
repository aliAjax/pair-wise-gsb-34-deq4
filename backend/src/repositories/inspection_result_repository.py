from src.repositories import store


class InspectionResultRepository:
    def _rows(self):
        return store.get_store()["inspectionResult"]

    def find_all(self):
        with store.lock():
            return [dict(row) for row in self._rows()]

    def find_by_task(self, task_id: int):
        with store.lock():
            return [dict(row) for row in self._rows() if row["task_id"] == task_id]

    def find_by_id(self, result_id: int):
        with store.lock():
            for row in self._rows():
                if row["id"] == result_id:
                    return dict(row)
        return None

    def create(self, row: dict):
        with store.lock():
            self._rows().append(row)
            return dict(row)
