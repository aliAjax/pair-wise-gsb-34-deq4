from pydantic import BaseModel


class HazardTicket(BaseModel):
    id: int | float
    result_id: int | float
    device_id: int | float | None = None
    severity: str
    owner_id: int | float
    deadline: str
    rectify_status: str
    rectify_note: str
    closed_at: str = ""
    # 同设备未关闭隐患合并累计的发现次数
    found_count: int = 1
    first_result_id: int | float | None = None
    latest_result_id: int | float | None = None
    created_at: str = ""
    updated_at: str = ""
