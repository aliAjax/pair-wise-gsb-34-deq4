"""进程内数据存储。

保留原 seed.py 的只读样例数据作为引导，真正的运行态数据在启动时通过
bootstrap 初始化，使旧任务样例也带上固定版本快照等新字段。
"""
import threading

from src.seed import seed as raw_seed

_lock = threading.RLock()
_store: dict = {}


def init_store(initial: dict) -> None:
    global _store
    with _lock:
        _store = initial


def get_store() -> dict:
    return _store


def lock():
    return _lock


def raw_seed_rows(kind: str):
    return raw_seed.get(kind, [])
