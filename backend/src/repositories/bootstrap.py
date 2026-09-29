"""运行态数据引导：把旧样例补齐为版本化结构，并预置可发布/已发布清单。"""
import copy

from src.constants.checklist_status import CHECKLIST_PUBLISHED
from src.constants.hazard_rectify_status import HAZARD_OPEN_STATUSES
from src.repositories import store

# v1：v1 版本，消火栓压力阈值较宽松；发布后物业又起草了收紧阈值的 v2。
_V1_PUBLISHED_AT = "2026-06-01T09:00:00Z"
_V2_CREATED_AT = "2026-06-05T09:00:00Z"

_CHECKLISTS = [
    {
        "id": 1,
        "task_type": "HYDRANT",
        "version": "1.0.0",
        "status": CHECKLIST_PUBLISHED,
        "remark": "首版消火栓巡检清单",
        "created_by": 1,
        "published_by": 1,
        "created_at": _V1_PUBLISHED_AT,
        "published_at": _V1_PUBLISHED_AT,
        "items": [
            {
                "item_code": "HYD-PRESSURE",
                "item_name": "栓口静水压力",
                "device_type": "HYDRANT",
                "rule": {"kind": "threshold", "min": 0.15, "max": 1.0, "unit": "MPa"},
                "fail_severity": "HIGH",
            },
            {
                "item_code": "HYD-LEAK",
                "item_name": "阀门渗漏检查",
                "device_type": "HYDRANT",
                "rule": {"kind": "options", "normal": ["NORMAL", "YES", "无渗漏"]},
                "fail_severity": "MEDIUM",
            },
            {
                "item_code": "HYD-ACCESS",
                "item_name": "通道占用检查",
                "device_type": "HYDRANT",
                "rule": {"kind": "options", "normal": ["NORMAL", "YES", "畅通"]},
                "fail_severity": "LOW",
            },
        ],
    },
    {
        "id": 2,
        "task_type": "HYDRANT",
        "version": "2.0.0",
        "status": "DRAFT",
        "remark": "收紧压力下限的草稿，尚未发布",
        "created_by": 1,
        "published_by": None,
        "created_at": _V2_CREATED_AT,
        "published_at": None,
        "items": [
            {
                "item_code": "HYD-PRESSURE",
                "item_name": "栓口静水压力",
                "device_type": "HYDRANT",
                "rule": {"kind": "threshold", "min": 0.25, "max": 1.0, "unit": "MPa"},
                "fail_severity": "CRITICAL",
            },
            {
                "item_code": "HYD-LEAK",
                "item_name": "阀门渗漏检查",
                "device_type": "HYDRANT",
                "rule": {"kind": "options", "normal": ["NORMAL", "YES", "无渗漏"]},
                "fail_severity": "HIGH",
            },
            {
                "item_code": "HYD-ACCESS",
                "item_name": "通道占用检查",
                "device_type": "HYDRANT",
                "rule": {"kind": "options", "normal": ["NORMAL", "YES", "畅通"]},
                "fail_severity": "MEDIUM",
            },
        ],
    },
]


def _snapshot(items):
    return copy.deepcopy(items)


def bootstrap() -> dict:
    """构造首版运行态数据：旧任务固定到 v1 快照，v2 仍是草稿。"""
    v1 = next(c for c in _CHECKLISTS if c["version"] == "1.0.0")

    buildings = copy.deepcopy(store.raw_seed_rows("building"))
    devices = copy.deepcopy(store.raw_seed_rows("fireDevice"))

    tasks = []
    for index, row in enumerate(copy.deepcopy(store.raw_seed_rows("inspectionTask")), start=1):
        if row.get("task_type") == "HYDRANT":
            row["checklist_version"] = v1["version"]
            row["checklist_version_id"] = v1["id"]
            row["version_pinned_at"] = _V1_PUBLISHED_AT
            row["version_notice"] = ""
            # 已领取（执行中）任务冻结 v1 快照，v2 发布后它的检查项也不会被换掉
            row["checklist_snapshot"] = _snapshot(v1["items"])
        else:
            row.setdefault("checklist_version_id", None)
            row.setdefault("version_pinned_at", "")
            row.setdefault("version_notice", "")
            row.setdefault("checklist_snapshot", [])
        row.setdefault("created_by", row.get("inspector_id", 1))
        tasks.append(row)

    results = []
    for row in copy.deepcopy(store.raw_seed_rows("inspectionResult")):
        row.setdefault("outcome", "")
        row.setdefault("checklist_version", "")
        row.setdefault("graded_at", "")
        results.append(row)

    hazards = []
    for row in copy.deepcopy(store.raw_seed_rows("hazardTicket")):
        # 旧样例状态归一到新整改状态枚举
        legacy = row.get("rectify_status")
        if legacy in HAZARD_OPEN_STATUSES or legacy in ("IN_PROGRESS", "SUBMITTED", "PLANNED"):
            row["rectify_status"] = "OPEN" if legacy != "IN_PROGRESS" else "RECTIFYING"
        row["closed_at"] = row.get("closed_at") or ""
        # 旧样例隐患没有设备关联，不参与“同设备未关闭合并”，避免干扰新流程
        row["device_id"] = None
        row.setdefault("found_count", 1)
        row.setdefault("first_result_id", row.get("result_id"))
        row.setdefault("latest_result_id", row.get("result_id"))
        row.setdefault("created_at", "2026-06-11T09:00:00Z")
        row.setdefault("updated_at", "2026-06-11T09:00:00Z")
        hazards.append(row)

    initial = {
        "building": buildings,
        "fireDevice": devices,
        "inspectionTask": tasks,
        "inspectionResult": results,
        "hazardTicket": hazards,
        "checklistVersion": copy.deepcopy(_CHECKLISTS),
    }
    store.init_store(initial)
    return initial
