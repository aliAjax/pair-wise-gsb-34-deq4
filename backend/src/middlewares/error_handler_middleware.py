from fastapi.responses import JSONResponse


def to_error_payload(exc):
    return {"code": getattr(exc, "code", "INTERNAL_ERROR"), "message": str(exc)}


async def error_handler_middleware(request, call_next):
    """兜底包装未在 controller/service 层处理的异常，禁止在单一位置吞掉业务异常。"""
    try:
        return await call_next(request)
    except Exception as exc:  # noqa: BLE001 - 全局错误处理中间件
        code = getattr(exc, "code", "INTERNAL_ERROR")
        return JSONResponse(status_code=500, content={"code": code, "message": str(exc)})
