from pydantic import BaseModel


class ChecklistItem(BaseModel):
    # 版本内唯一的检查项编码，任务结果按它与快照项对齐
    item_code: str
    item_name: str
    rule_type: str
    device_type: str
    severity: str
    # NUMERIC 规则参数
    min_value: float | None = None
    max_value: float | None = None
    critical_min: float | None = None
    critical_max: float | None = None
    # CHOICE 规则参数：命中即为正常
    allowed_values: list[str] = []
    # TEXT 规则参数：等于该值判定异常
    abnormal_value: str | None = None
    required: bool = True


class ChecklistVersion(BaseModel):
    id: int | float
    # 同 task_type + scope_key 下版本号递增，发布后不可变
    task_type: str
    scope_key: str = "DEFAULT"
    version: int
    status: str  # DRAFT / PUBLISHED
    items: list[ChecklistItem] = []
    published_at: str = ""
    published_by: int | float | None = None
    created_at: str = ""
    created_by: int | float | None = None
    remark: str = ""
