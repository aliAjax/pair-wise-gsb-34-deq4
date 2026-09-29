from pydantic import BaseModel


class ChecklistItem(BaseModel):
    item_code: str
    item_name: str = ""
    device_type: str | None = None
    rule: dict = {}
    fail_severity: str | None = None


class ChecklistVersion(BaseModel):
    id: int | float
    task_type: str
    version: str
    status: str
    remark: str = ""
    created_by: int | float = 1
    published_by: int | float | None = None
    created_at: str = ""
    published_at: str | None = None
    archived_at: str | None = None
    items: list[ChecklistItem] = []
