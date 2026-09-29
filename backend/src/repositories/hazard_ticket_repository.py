from src.repositories import store


class HazardTicketRepository:
    def _rows(self):
        return store.get_store()["hazardTicket"]

    def find_all(self):
        with store.lock():
            return [dict(row) for row in self._rows()]

    def find_by_id(self, ticket_id: int):
        with store.lock():
            for row in self._rows():
                if row["id"] == ticket_id:
                    return dict(row)
        return None

    def find_open_by_device(self, device_id: int, open_statuses):
        """同一设备当前存在的未关闭隐患单（合并目标）。"""
        with store.lock():
            rows = [
                dict(row) for row in self._rows()
                if row.get("device_id") == device_id and row["rectify_status"] in tuple(open_statuses)
            ]
        return sorted(rows, key=lambda r: r["id"])

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
