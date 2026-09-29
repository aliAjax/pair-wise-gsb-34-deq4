from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from src.services.inspection_task_service import InspectionTaskService
from src.types.inspection_task_payload import InspectionSubmitPayload, InspectionTaskCreatePayload
from src.utils.domain_error import DomainError

service = InspectionTaskService()


def list_inspection_task():
    return service.list()


def get_inspection_task(task_id: int):
    try:
        return service.get(task_id)
    except DomainError as exc:
        raise _as_http(exc)


def create_inspection_task(payload: InspectionTaskCreatePayload):
    try:
        # 建任务即固定当时已发布清单版本；版本并发提示在响应 version_notice 中
        return service.create(jsonable_encoder(payload))
    except DomainError as exc:
        raise _as_http(exc)


def submit_inspection_task(task_id: int, payload: InspectionSubmitPayload):
    try:
        # 按任务固定版本判级，异常项生成/合并隐患单
        return service.submit(task_id, jsonable_encoder(payload))
    except DomainError as exc:
        raise _as_http(exc)


def _as_http(exc: DomainError):
    not_found = ("TASK_NOT_FOUND", "CHECKLIST_NOT_FOUND")
    conflict = ("TASK_ALREADY_SUBMITTED", "CHECKLIST_ALREADY_PUBLISHED")
    status = 404 if exc.code in not_found else 409 if exc.code in conflict else 400
    return HTTPException(status_code=status, detail={"code": exc.code, "message": str(exc)})
