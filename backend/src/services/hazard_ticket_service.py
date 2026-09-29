from __future__ import annotations
from src.constants.error_codes import HAZARD_NOT_FOUND, HAZARD_ALREADY_CLOSED
from src.constants.error_messages import ERROR_MESSAGES
from src.constants.hazard_rectify_status import HAZARD_OPEN_STATUSES, HAZARD_CLOSED
from src.exceptions.service_error import ServiceError
from src.repositories.hazard_ticket_repository import HazardTicketRepository
from src.constructors.hazard_ticket_factory import create_hazard_ticket_dto
from src.utils.clock import utc_now_iso
from src.utils.audit import record_audit

# 等级优先级：合并到原单后，若本次异常更严重则抬升等级
_SEVERITY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


class HazardTicketService:
    def __init__(self):
        self.repo = HazardTicketRepository()

    def list(self):
        return self.repo.find_all()

    def get(self, ticket_id: int):
        row = self.repo.find_by_id(ticket_id)
        if row is None:
            raise ServiceError(
                HAZARD_NOT_FOUND,
                ERROR_MESSAGES[HAZARD_NOT_FOUND].format(ticket_id=ticket_id),
                http_status=404,
            )
        return row

    def raise_for_abnormal_result(self, result: dict, device_id: int | None, severity: str,
                                  actor_id: int = 1, moment: str | None = None) -> dict:
        """异常结果生成隐患单。

        同一设备已有未关闭隐患时合并：累计 found_count、刷新最近结果与时间，
        等级就高不就低；否则新建单据。
        """
        now = moment or utc_now_iso()
        existing = self.repo.find_open_by_device(device_id, HAZARD_OPEN_STATUSES) if device_id is not None else []
        if existing:
            return self._merge(existing[0], result, severity, actor_id, now)
        return self._create(result, device_id, severity, actor_id, now)

    def _create(self, result, device_id, severity, actor_id, now) -> dict:
        max_id = max([row["id"] for row in self.repo.find_all()] or [0])
        row = create_hazard_ticket_dto(
            id=max_id + 1,
            result_id=result["id"],
            first_result_id=result["id"],
            latest_result_id=result["id"],
            device_id=device_id,
            severity=severity,
            owner_id=actor_id,
            deadline="",
            rectify_status="OPEN",
            rectify_note="",
            closed_at="",
            found_count=1,
            created_at=now,
            updated_at=now,
        )
        saved = self.repo.create(row)
        record_audit(
            actor_id,
            "HazardTicket.create",
            "HazardTicket",
            saved["id"],
            {"device_id": device_id, "result_id": result["id"], "severity": severity,
             "found_count": 1, "merged": False},
            created_at=now,
        )
        return saved

    def _merge(self, ticket: dict, result: dict, severity: str, actor_id: int, now: str) -> dict:
        previous_count = ticket["found_count"]
        ticket["found_count"] = previous_count + 1
        ticket["latest_result_id"] = result["id"]
        ticket["updated_at"] = now
        # 隐患等级就高不就低，避免新异常被旧的较低等级掩盖
        if _SEVERITY_RANK.get(severity, 0) > _SEVERITY_RANK.get(ticket["severity"], 0):
            ticket["severity"] = severity
        saved = self.repo.update(ticket)
        record_audit(
            actor_id,
            "HazardTicket.merge",
            "HazardTicket",
            saved["id"],
            {"device_id": saved.get("device_id"), "merged_result_id": result["id"],
             "previous_found_count": previous_count, "found_count": saved["found_count"],
             "severity": saved["severity"]},
            created_at=now,
        )
        return saved

    def close(self, ticket_id: int, actor_id: int = 1, note: str = "", moment: str | None = None) -> dict:
        ticket = self.repo.find_by_id(ticket_id)
        if ticket is None:
            raise ServiceError(
                HAZARD_NOT_FOUND,
                ERROR_MESSAGES[HAZARD_NOT_FOUND].format(ticket_id=ticket_id),
                http_status=404,
            )
        if ticket["rectify_status"] == HAZARD_CLOSED:
            raise ServiceError(
                HAZARD_ALREADY_CLOSED,
                ERROR_MESSAGES[HAZARD_ALREADY_CLOSED].format(ticket_id=ticket_id),
                http_status=409,
            )
        now = moment or utc_now_iso()
        ticket["rectify_status"] = HAZARD_CLOSED
        ticket["closed_at"] = now
        ticket["updated_at"] = now
        if note:
            ticket["rectify_note"] = note
        saved = self.repo.update(ticket)
        record_audit(
            actor_id,
            "HazardTicket.close",
            "HazardTicket",
            saved["id"],
            {"device_id": saved.get("device_id"), "found_count": saved["found_count"],
             "closed_at": now},
            created_at=now,
        )
        return saved
