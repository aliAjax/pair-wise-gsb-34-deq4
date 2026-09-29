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
    # 建任务时固定的清单版本主键与版本号，执行期间不再随发布变化
    checklist_version_id: int | float | None = None
    version_no: int | None = None
    # 当时版本检查项快照（含判级规则），提交时按此快照判定
    pinned_items: list = []
    created_at: str = ""
    created_by: int | float | None = None
    # 发布与建任务并发时，记录给创建人的提示
    version_notice: str = ""
