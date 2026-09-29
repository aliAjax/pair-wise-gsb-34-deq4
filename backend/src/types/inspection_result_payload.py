from pydantic import BaseModel


class InspectionEntryPayload(BaseModel):
    device_id: int
    item_code: str
    measured_value: str = ""
    photo_url: str = ""
    note: str = ""


InspectionResultPayload = dict
