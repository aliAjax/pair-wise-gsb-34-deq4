from src.constants.error_codes import ERROR_CODES
from src.constants.error_messages import ERROR_MESSAGES


class DomainError(Exception):
    """service/controller 分层包装的业务异常基类，错误码集中在 constants/error_codes。"""

    def __init__(self, code: str, message: str | None = None):
        self.code = code if code in ERROR_CODES else "VALIDATION_FAILED"
        super().__init__(message or ERROR_MESSAGES.get(self.code, code))
