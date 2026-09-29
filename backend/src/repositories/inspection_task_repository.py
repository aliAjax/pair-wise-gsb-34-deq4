from src.repositories import store


class InspectionTaskRepository:
    def _rows(self):
        return store.get_store()["inspectionTask"]

    def find_all(self):
        with store.lock():
            return [dict(row) for row in self._rows()]

    def find_by_id(self, task_id: int):
        with store.lock():
            for row in self._rows():
                if row["id"] == task_id:
                    return dict(row)
        return None

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
