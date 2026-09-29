"""进程内数据存储。

清单版本化要求发布、建任务、提交、合并均产生状态流转与可追溯日志，
因此统一在 store 中维护自增主键、并发锁和审计日志；repository 层只做访问封装。
"""
import threading
from datetime import datetime, timezone

from src.seed import seed


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DataStore:
    def __init__(self):
        self._lock = threading.RLock()
        self.building = [dict(row) for row in seed["building"]]
        self.fire_device = [dict(row) for row in seed["fireDevice"]]
        self.inspection_task = [dict(row) for row in seed["inspectionTask"]]
        self.inspection_result = [dict(row) for row in seed["inspectionResult"]]
        self.hazard_ticket = [dict(row) for row in seed["hazardTicket"]]
        self.checklist_version = []
        self.audit_log = []
        # 种子数据 id 从 1 开始，序列必须从其最大 id 之后起跳，避免新记录撞号
        self._sequences = {
            key: max((int(row["id"]) for row in rows), default=0)
            for key, rows in (
                ("building", self.building),
                ("fire_device", self.fire_device),
                ("inspection_task", self.inspection_task),
                ("inspection_result", self.inspection_result),
                ("hazard_ticket", self.hazard_ticket),
            )
        }

    @property
    def lock(self) -> threading.RLock:
        return self._lock

    def next_id(self, key: str) -> int:
        with self._lock:
            self._sequences[key] = self._sequences.get(key, 0) + 1
            return self._sequences[key]

    def append_log(self, actor: str, action: str, target_type: str, target_id, detail: str = ""):
        with self._lock:
            log = {
                "id": self.next_id("audit_log"),
                "actor": str(actor),
                "action": action,
                "target_type": target_type,
                "target_id": str(target_id),
                "detail": detail,
                "created_at": now_iso(),
            }
            self.audit_log.append(log)
            return log


store = DataStore()
