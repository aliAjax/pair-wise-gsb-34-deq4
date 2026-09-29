from src.exceptions.controller_error import ControllerError
from src.exceptions.domain_error import DomainError
from src.services.checklist_version_service import ChecklistVersionService
from src.types.checklist_payload import ChecklistVersionCreatePayload

service = ChecklistVersionService()


def list_checklist_version():
    try:
        return service.list()
    except DomainError as exc:
        raise ControllerError(exc) from exc


def create_checklist_version(payload: ChecklistVersionCreatePayload):
    try:
        return service.create_draft(payload)
    except DomainError as exc:
        raise ControllerError(exc) from exc


def publish_checklist_version(version_id: int, actor_id: int = 1):
    try:
        return service.publish(version_id, actor_id=actor_id)
    except DomainError as exc:
        raise ControllerError(exc) from exc
