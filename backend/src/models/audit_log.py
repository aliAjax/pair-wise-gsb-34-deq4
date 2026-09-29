from pydantic import BaseModel


class AuditLog(BaseModel):
    id: int | float
    actor: str
    action: str
    target_type: str
    target_id: str
    detail: str = ""
    created_at: str = ""
