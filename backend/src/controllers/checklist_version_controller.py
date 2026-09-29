from fastapi.encoders import jsonable_encoder

from src.constants.error_codes import ERROR_CODES
from src.services.checklist_version_service import ChecklistVersionService
from src.types.checklist_version_payload import ChecklistVersionPayload
from src.utils.domain_error import DomainError

service = ChecklistVersionService()


def list_checklist_version(task_type: str | None = None):
    try:
        return service.list_versions(task_type)
    except DomainError as exc:
        # controller 层包装：保证错误码来自集中维护的 error_codes
        raise _as_http(exc)


def get_current_checklist(task_type: str):
    try:
        return service.get_current(task_type)
    except DomainError as exc:
        raise _as_http(exc)


def create_checklist_draft(payload: ChecklistVersionPayload):
    try:
        return service.create_draft(jsonable_encoder(payload))
    except DomainError as exc:
        raise _as_http(exc)


def publish_checklist(version_id: int):
    try:
        return service.publish(version_id)
    except DomainError as exc:
        raise _as_http(exc)


def _as_http(exc: DomainError):
    from fastapi import HTTPException

    status = 404 if exc.code in (ERROR_CODES["CHECKLIST_NOT_FOUND"],) else 409
    if exc.code == "VALIDATION_FAILED":
        status = 400
    return HTTPException(status_code=status, detail={"code": exc.code, "message": str(exc)})
