from fastapi import APIRouter

from src.controllers.hazard_ticket_controller import (
    list_hazard_ticket,
    get_hazard_ticket,
    close_hazard_ticket,
)

router = APIRouter(prefix="/api/hazard-ticket", tags=["HazardTicket"])
router.get("")(list_hazard_ticket)
router.get("/{ticket_id}")(get_hazard_ticket)
router.post("/{ticket_id}/close")(close_hazard_ticket)
