from src.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:
    def __init__(self):
        self.repo = AuditLogRepository()

    def list(self, target_type: str | None = None, target_id: str | None = None):
        rows = self.repo.find_all()
        if target_type:
            rows = [row for row in rows if row["target_type"] == target_type]
        if target_id is not None:
            rows = [row for row in rows if row["target_id"] == str(target_id)]
        return rows
