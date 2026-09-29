import copy

from src.constants.log_templates import LOG_TEMPLATES
from src.repositories.hazard_ticket_repository import HazardTicketRepository
from src.repositories.store import now_iso, store
from src.utils.domain_error import DomainError


class HazardTicketService:
    def __init__(self):
        self.repo = HazardTicketRepository()

    def list(self):
        return self.repo.find_all()

    def close(self, ticket_id, payload: dict | None = None, actor=1):
        """复验关闭：关闭后不再参与同设备隐患合并。"""
        ticket = self.repo.find_by_id(ticket_id)
        if ticket is None:
            raise DomainError("VALIDATION_FAILED", f"hazard ticket {ticket_id} not found")
        with store.lock:
            rows = store.hazard_ticket
            for row in rows:
                if row["id"] == ticket_id:
                    row["rectify_status"] = "CLOSED"
                    row["closed_at"] = now_iso()
                    row["rectify_note"] = (payload or {}).get("rectify_note", row.get("rectify_note", ""))
                    ticket = copy.deepcopy(row)
                    break
            store.append_log(
                actor, LOG_TEMPLATES["HazardTicket"][2], "HazardTicket", ticket_id,
                f"review closed, total found_count={ticket['found_count']} device={ticket.get('device_id')}",
            )
        return ticket
