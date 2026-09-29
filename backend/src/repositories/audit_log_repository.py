from src.repositories.store import store


class AuditLogRepository:
    def find_all(self):
        with store.lock:
            return [dict(row) for row in store.audit_log]

    def find_by_target(self, target_type: str, target_id):
        with store.lock:
            return [
                dict(row)
                for row in store.audit_log
                if row["target_type"] == target_type and row["target_id"] == str(target_id)
            ]
