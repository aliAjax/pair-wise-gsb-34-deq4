import threading
from contextlib import contextmanager

# 清单发布与建任务可能并发发生；对同一 task_type 加锁，
# 保证“建任务固定当时已发布版本”的读-写过程不交错。
_locks_guard = threading.Lock()
_named_locks: dict[str, threading.Lock] = {}


def get_named_lock(name: str) -> threading.Lock:
    with _locks_guard:
        lock = _named_locks.get(name)
        if lock is None:
            lock = threading.Lock()
            _named_locks[name] = lock
        return lock


@contextmanager
def named_lock(name: str):
    lock = get_named_lock(name)
    lock.acquire()
    try:
        yield
    finally:
        lock.release()
