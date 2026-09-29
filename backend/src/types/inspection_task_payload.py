from pydantic import BaseModel, Field


class InspectionTaskCreatePayload(BaseModel):
    building_id: int
    inspector_id: int | None = None
    plan_date: str = ""
    task_type: str
    # 前端打开创建表单时看到的已发布版本；发布并发时用于检测并提示创建人
    expected_version_id: int | None = None


class InspectionEntryPayload(BaseModel):
    device_id: int
    item_code: str
    measured_value: str = ""
    photo_url: str = ""
    note: str = ""


class InspectionSubmitPayload(BaseModel):
    entries: list[InspectionEntryPayload] = Field(default_factory=list)
