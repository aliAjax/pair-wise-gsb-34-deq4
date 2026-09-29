from src.utils.audit import list_audit


def list_audit_log(action: str | None = None, target_type: str | None = None, limit: int = 100):
    """审计追溯：发布、任务完成、隐患合并/关闭等领域动作均可在此查询。"""
    return list_audit(limit=limit, action=action, target_type=target_type)
