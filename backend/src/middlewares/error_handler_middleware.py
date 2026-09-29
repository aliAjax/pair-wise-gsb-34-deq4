from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.exceptions.domain_error import DomainError


def to_error_payload(exc):
    """service/controller 抛出的领域异常统一转换为错误响应结构。"""
    return {"code": getattr(exc, "code", "INTERNAL_ERROR"), "message": str(exc)}


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """全局兜底异常处理；业务异常仍由 service/controller 各自包装，这里不吞语义。"""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except DomainError as exc:
            return JSONResponse(status_code=getattr(exc, "http_status", 400),
                                content=to_error_payload(exc))
        except Exception as exc:  # noqa: BLE001 - 全局兜底必须覆盖未预期异常
            return JSONResponse(status_code=500,
                                content={"code": "INTERNAL_ERROR", "message": str(exc)})
