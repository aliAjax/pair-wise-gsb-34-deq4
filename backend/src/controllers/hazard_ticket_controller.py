from src.exceptions.controller_error import ControllerError
from src.exceptions.domain_error import DomainError
from src.services.hazard_ticket_service import HazardTicketService

service = HazardTicketService()


def list_hazard_ticket():
    try:
        return service.list()
    except DomainError as exc:
        raise ControllerError(exc) from exc


def get_hazard_ticket(ticket_id: int):
    try:
        return service.get(ticket_id)
    except DomainError as exc:
        raise ControllerError(exc) from exc


def close_hazard_ticket(ticket_id: int, actor_id: int = 1, note: str = ""):
    """复验关闭：关闭后该设备再次发现异常将新建单据而不是继续合并。"""
    try:
        return service.close(ticket_id, actor_id=actor_id, note=note)
    except DomainError as exc:
        raise ControllerError(exc) from exc
