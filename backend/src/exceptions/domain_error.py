class DomainError(Exception):
    """所有领域异常基类，携带错误码与 http 状态，供错误处理中间件统一包装。"""

    def __init__(self, code: str, message: str, http_status: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.http_status = http_status
