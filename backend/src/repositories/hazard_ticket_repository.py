import copy

from src.repositories.store import now_iso, store


class HazardTicketRepository:
    def find_all(self):
        with store.lock:
            return copy.deepcopy(store.hazard_ticket)

    def find_open_by_device(self, device_id):
        """查找同一设备尚未关闭（rectify_status != CLOSED）的隐患单。"""
        with store.lock:
            for row in store.hazard_ticket:
                if row.get("device_id") == device_id and row["rectify_status"] != "CLOSED":
                    return copy.deepcopy(row)
        return None

    def find_by_id(self, ticket_id):
        with store.lock:
            for row in store.hazard_ticket:
                if row["id"] == ticket_id:
                    return copy.deepcopy(row)
        return None

    def create(self, payload: dict) -> dict:
        with store.lock:
            row = {
                "id": store.next_id("hazard_ticket"),
                "result_id": payload["result_id"],
                "device_id": payload.get("device_id"),
                "severity": payload["severity"],
                "owner_id": payload.get("owner_id", 1),
                "deadline": payload.get("deadline", ""),
                "rectify_status": "OPEN",
                "rectify_note": "",
                "closed_at": "",
                "found_count": 1,
                "merged_result_ids": [payload["result_id"]],
                "last_found_at": now_iso(),
                "created_at": now_iso(),
            }
            store.hazard_ticket.append(row)
            return copy.deepcopy(row)

    def merge_find(self, ticket_id: int, result_id, severity: str) -> dict | None:
        """把新的异常发现合并进未关闭隐患单：累计发现次数、取最高等级。"""
        rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        with store.lock:
            for row in store.hazard_ticket:
                if row["id"] == ticket_id and row["rectify_status"] != "CLOSED":
                    row["found_count"] += 1
                    if rank.get(severity, 0) > rank.get(row["severity"], 0):
                        row["severity"] = severity
                    if result_id not in row["merged_result_ids"]:
                        row["merged_result_ids"].append(result_id)
                    row["last_found_at"] = now_iso()
                    return copy.deepcopy(row)
        return None
