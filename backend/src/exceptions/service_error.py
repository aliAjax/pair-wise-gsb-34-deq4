from src.exceptions.domain_error import DomainError


class ServiceError(DomainError):
    """service 层抛出的业务异常：禁止把异常处理全部塞进全局中间件。"""
