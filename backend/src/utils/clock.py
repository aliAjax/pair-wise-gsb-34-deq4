import itertools
from datetime import datetime, timezone


def utc_now_iso() -> str:
    """统一的 UTC 时间戳（毫秒精度），发布/建任务并发性判定依赖同一时钟。"""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class IdGenerator:
    """进程内自增 ID，按实体序列隔离，避免写操作之间相互覆盖 ID。"""

    def __init__(self):
        self._sequences = {}

    def next_id(self, scope: str) -> int:
        if scope not in self._sequences:
            self._sequences[scope] = itertools.count(1)
        return next(self._sequences[scope])
