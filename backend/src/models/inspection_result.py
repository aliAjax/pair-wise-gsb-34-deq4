from pydantic import BaseModel


class InspectionResult(BaseModel):
    id: int | float
    task_id: int | float
    device_id: int | float | None
    item_code: str
    result_status: str
    measured_value: str
    photo_url: str
    note: str
    # 按任务固定版本判级的结论
    outcome: str = ""
    checklist_version: str = ""
    graded_at: str = ""
