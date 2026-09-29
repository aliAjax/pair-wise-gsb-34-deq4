import copy

from src.repositories.store import store


class BuildingRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.building)

    def find_by_id(self, building_id):
        with store.lock:
            for row in store.building:
                if row["id"] == building_id:
                    return copy.deepcopy(row)
        return None
