from src.services.audit_log_service import AuditLogService

service = AuditLogService()


def list_audit_log(target_type: str | None = None, target_id: str | None = None):
    return service.list(target_type, target_id)
