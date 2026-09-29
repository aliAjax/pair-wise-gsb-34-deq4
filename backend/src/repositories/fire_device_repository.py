import copy

from src.repositories.store import store


class FireDeviceRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.fire_device)

    def find_by_id(self, device_id):
        with store.lock:
            for row in store.fire_device:
                if row["id"] == device_id:
                    return copy.deepcopy(row)
        return None

    def update_status(self, device_id, status: str):
        with store.lock:
            for row in store.fire_device:
                if row["id"] == device_id:
                    row["status"] = status
                    return copy.deepcopy(row)
        return None
