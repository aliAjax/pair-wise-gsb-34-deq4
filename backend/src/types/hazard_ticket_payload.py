from pydantic import BaseModel


class HazardTicketClosePayload(BaseModel):
    rectify_note: str = ""


HazardTicketPayload = dict
