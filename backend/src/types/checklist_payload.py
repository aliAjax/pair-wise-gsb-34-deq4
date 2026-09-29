from pydantic import BaseModel, Field


class ChecklistItemPayload(BaseModel):
    item_code: str
    item_name: str = ""
    device_type: str | None = None
    rule: dict = Field(default_factory=dict)
    fail_severity: str | None = None


class ChecklistVersionCreatePayload(BaseModel):
    task_type: str
    version: str
    remark: str = ""
    created_by: int = 1
    items: list[ChecklistItemPayload] = Field(default_factory=list)


class ChecklistItemInput(BaseModel):
    """提交巡检结果时的单条目输入。"""
    item_code: str
    measured_value: str = ""
    result_status: str = "DONE"
    photo_url: str = ""
    note: str = ""
    device_id: int | None = None


class TaskSubmitPayload(BaseModel):
    """巡检员提交：只携带本次检查项录入值，判级完全由任务固定版本决定。"""
    results: list[ChecklistItemInput] = Field(default_factory=list)
    actor_id: int = 1
