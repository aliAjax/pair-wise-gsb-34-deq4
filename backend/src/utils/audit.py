import threading

from src.utils.clock import utc_now_iso

# 进程内审计台账：发布、任务完成、隐患合并等所有写操作都可追溯。
# 与 audit_log_middleware（仅记录 HTTP 请求）互补，这里记录的是领域动作。
_audit_rows: list[dict] = []
_audit_lock = threading.Lock()
_audit_seq = 0


def record_audit(actor_id, action: str, target_type: str, target_id, detail: dict | None = None,
                 created_at: str | None = None) -> dict:
    global _audit_seq
    with _audit_lock:
        _audit_seq += 1
        row = {
            "id": _audit_seq,
            "actor_id": actor_id,
            "action": action,
            "target_type": target_type,
            "target_id": str(target_id),
            "detail": detail or {},
            "created_at": created_at or utc_now_iso(),
        }
        _audit_rows.append(row)
        return dict(row)


def list_audit(limit: int = 100, action: str | None = None, target_type: str | None = None) -> list[dict]:
    with _audit_lock:
        rows = list(reversed(_audit_rows))
    if action:
        rows = [r for r in rows if r["action"] == action]
    if target_type:
        rows = [r for r in rows if r["target_type"] == target_type]
    return rows[:limit]


def reset_audit() -> None:
    """测试辅助：清空审计台账。"""
    global _audit_seq
    with _audit_lock:
        _audit_rows.clear()
        _audit_seq = 0
