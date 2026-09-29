from src.repositories import store


class BuildingRepository:
    def find_all(self):
        with store.lock():
            return [dict(row) for row in store.get_store()["building"]]

    def find_by_id(self, building_id: int):
        with store.lock():
            for row in store.get_store()["building"]:
                if row["id"] == building_id:
                    return dict(row)
        return None
