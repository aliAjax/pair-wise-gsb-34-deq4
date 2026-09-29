from src.repositories import store


class FireDeviceRepository:
    def _rows(self):
        return store.get_store()["fireDevice"]

    def find_all(self):
        with store.lock():
            return [dict(row) for row in self._rows()]

    def find_by_id(self, device_id: int):
        with store.lock():
            for row in self._rows():
                if row["id"] == device_id:
                    return dict(row)
        return None

    def find_by_building_and_type(self, building_id: int, device_type: str):
        with store.lock():
            return [
                dict(row) for row in self._rows()
                if row["building_id"] == building_id and row["device_type"] == device_type
            ]
