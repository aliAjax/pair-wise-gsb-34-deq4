from pydantic import BaseModel
class HazardTicket(BaseModel):
    id: int | float
    result_id: int | float
    severity: str
    owner_id: int | float
    deadline: str
    rectify_status: str
    rectify_note: str
    closed_at: str
    # 同设备重复隐患合并时冗余设备，便于查重与展示
    device_id: int | float | None = None
    # 发现次数：每合并一次同设备未关闭隐患累计 +1
    found_count: int = 1
    merged_result_ids: list = []
    last_found_at: str = ""
    created_at: str = ""
