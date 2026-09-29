from src.exceptions.controller_error import ControllerError
from src.exceptions.domain_error import DomainError
from src.services.inspection_task_service import InspectionTaskService
from src.types.inspection_task_payload import InspectionTaskCreatePayload
from src.types.checklist_payload import TaskSubmitPayload

service = InspectionTaskService()


def list_inspection_task():
    try:
        return service.list()
    except DomainError as exc:
        raise ControllerError(exc) from exc


def get_inspection_task(task_id: int):
    try:
        return service.get(task_id)
    except DomainError as exc:
        raise ControllerError(exc) from exc


def create_inspection_task(payload: InspectionTaskCreatePayload):
    """建任务时固定当前已发布清单版本；与发布并发时返回 version_notice 提示。"""
    try:
        return service.create(payload)
    except DomainError as exc:
        raise ControllerError(exc) from exc


def submit_inspection_task(task_id: int, payload: TaskSubmitPayload):
    """按任务固定版本判级提交，异常项生成/合并隐患单。"""
    try:
        return service.submit(task_id, payload)
    except DomainError as exc:
        raise ControllerError(exc) from exc
