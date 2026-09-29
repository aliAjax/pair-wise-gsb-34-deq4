from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from src.services.hazard_ticket_service import HazardTicketService
from src.types.hazard_ticket_payload import HazardTicketClosePayload
from src.utils.domain_error import DomainError

service = HazardTicketService()


def list_hazard_ticket():
    return service.list()


def close_hazard_ticket(ticket_id: int, payload: HazardTicketClosePayload):
    try:
        return service.close(ticket_id, jsonable_encoder(payload))
    except DomainError as exc:
        raise HTTPException(status_code=400, detail={"code": exc.code, "message": str(exc)})
