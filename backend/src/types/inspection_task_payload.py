from pydantic import BaseModel


class InspectionTaskCreatePayload(BaseModel):
    building_id: int
    inspector_id: int
    plan_date: str
    task_type: str
    created_by: int = 1
