from pydantic import BaseModel


class InspectionTask(BaseModel):
    id: int | float
    building_id: int | float
    inspector_id: int | float
    plan_date: str
    task_type: str
    status: str
    checklist_version: str
    finished_at: str
    # 建任务时固定的清单版本与检查项快照
    checklist_version_id: int | float | None = None
    version_pinned_at: str = ""
    created_by: int | float = 1
    version_notice: str = ""
