from src.exceptions.domain_error import DomainError


class ControllerError(DomainError):
    """controller 层再次包装 service 异常，保留错误码并补充 http 语义。"""

    def __init__(self, source: DomainError, http_status: int | None = None):
        super().__init__(source.code, source.message, http_status or source.http_status)
