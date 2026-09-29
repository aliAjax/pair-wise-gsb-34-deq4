from pydantic import BaseModel, Field


class ChecklistItemPayload(BaseModel):
    item_code: str
    item_name: str = ""
    rule_type: str
    device_type: str | None = None
    severity: str = "MEDIUM"
    min_value: float | None = None
    max_value: float | None = None
    critical_min: float | None = None
    critical_max: float | None = None
    allowed_values: list[str] = Field(default_factory=list)
    abnormal_value: str | None = None
    required: bool = True


class ChecklistVersionPayload(BaseModel):
    task_type: str
    scope_key: str = "DEFAULT"
    remark: str = ""
    items: list[ChecklistItemPayload]
