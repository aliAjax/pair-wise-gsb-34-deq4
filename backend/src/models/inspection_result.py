from pydantic import BaseModel
class InspectionResult(BaseModel):
    id: int | float
    task_id: int | float
    device_id: int | float
    item_code: str
    result_status: str
    measured_value: str
    photo_url: str
    note: str
    # 提交时按任务固定版本判出的等级：NORMAL / LOW / MEDIUM / HIGH / CRITICAL
    judged_severity: str = ""
    checklist_version: str = ""
    submitted_at: str = ""
