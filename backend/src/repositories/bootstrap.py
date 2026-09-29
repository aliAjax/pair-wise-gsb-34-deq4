"""清单版本初始数据与存量任务版本固化。

启动时为每种设备类型建立已发布 v1 清单（含判级规则），并把存量任务
快照到当时版本，保证"执行期间不受后续发布影响"对老任务同样成立。
"""
from src.constants.hazard_severity import HazardSeverity
from src.repositories.store import now_iso, store


def _item(item_code, item_name, rule_type, device_type, severity, **params):
    row = {
        "item_code": item_code,
        "item_name": item_name,
        "rule_type": rule_type,
        "device_type": device_type,
        "severity": severity,
        "min_value": None,
        "max_value": None,
        "critical_min": None,
        "critical_max": None,
        "allowed_values": [],
        "abnormal_value": None,
        "required": True,
    }
    row.update(params)
    return row


_SEED_VERSIONS = [
    {
        "task_type": "HYDRANT",
        "version": 1,
        "status": "PUBLISHED",
        "remark": "消火栓首版检查清单",
        "items": [
            _item("H_PRESSURE", "管网压力(MPa)", "NUMERIC", "HYDRANT", HazardSeverity[2],
                  min_value=0.20, max_value=0.80, critical_max=1.00),
            _item("H_BOX", "栓箱完好", "CHOICE", "HYDRANT", HazardSeverity[1],
                  allowed_values=["INTACT"]),
            _item("H_WATER", "供水状态", "TEXT", "HYDRANT", HazardSeverity[2],
                  abnormal_value="NO_WATER"),
        ],
    },
    {
        "task_type": "SMOKE_DETECTOR",
        "version": 1,
        "status": "PUBLISHED",
        "remark": "烟感首版检查清单",
        "items": [
            _item("SD_TEST", "联动测试", "CHOICE", "SMOKE_DETECTOR", HazardSeverity[2],
                  allowed_values=["PASS"]),
            _item("SD_LED", "指示灯", "TEXT", "SMOKE_DETECTOR", HazardSeverity[0],
                  abnormal_value="OFF"),
        ],
    },
    {
        "task_type": "SPRINKLER",
        "version": 1,
        "status": "PUBLISHED",
        "remark": "喷淋首版检查清单",
        "items": [
            _item("SP_PRESSURE", "末端水压(MPa)", "NUMERIC", "SPRINKLER", HazardSeverity[2],
                  min_value=0.05, max_value=0.60, critical_min=0.03),
        ],
    },
    {
        # 物业编辑中的下一版：未发布，建任务不应取到它
        "task_type": "HYDRANT",
        "version": 2,
        "status": "DRAFT",
        "remark": "消火栓清单改版（草稿）",
        "items": [
            _item("H_PRESSURE", "管网压力(MPa)", "NUMERIC", "HYDRANT", HazardSeverity[3],
                  min_value=0.25, max_value=0.70, critical_max=0.90),
            _item("H_BOX", "栓箱完好与封签", "CHOICE", "HYDRANT", HazardSeverity[2],
                  allowed_values=["INTACT"]),
            _item("H_SEAL", "铅封检查", "TEXT", "HYDRANT", HazardSeverity[1],
                  abnormal_value="BROKEN"),
        ],
    },
]


def bootstrap():
    with store.lock:
        if store.checklist_version:
            return
        ts = now_iso()
        published_index = {}
        for spec in _SEED_VERSIONS:
            version_id = store.next_id("checklist_version")
            row = {
                "id": version_id,
                "task_type": spec["task_type"],
                "scope_key": "DEFAULT",
                "version": spec["version"],
                "status": spec["status"],
                "items": spec["items"],
                "published_at": ts if spec["status"] == "PUBLISHED" else "",
                "published_by": 1 if spec["status"] == "PUBLISHED" else None,
                "created_at": ts,
                "created_by": 1,
                "remark": spec["remark"],
            }
            store.checklist_version.append(row)
            if spec["status"] == "PUBLISHED":
                published_index[spec["task_type"]] = row

        # 存量任务固定到各自设备类型的已发布版本，避免被后续发布换掉检查项
        for task in store.inspection_task:
            pinned = published_index.get(task.get("task_type"))
            task.setdefault("pinned_items", [])
            task.setdefault("version_notice", "")
            task.setdefault("created_by", task.get("inspector_id"))
            task.setdefault("created_at", task.get("plan_date", ts))
            if pinned:
                task["checklist_version_id"] = pinned["id"]
                task["version_no"] = pinned["version"]
                task["checklist_version"] = f"v{pinned['version']}"
                task["pinned_items"] = [dict(item) for item in pinned["items"]]

        # 隐患单补设备与发现次数字段；第三张演示已关闭单（不再参与合并）
        result_device = {r["id"]: r["device_id"] for r in store.inspection_result}
        for idx, ticket in enumerate(store.hazard_ticket):
            ticket["device_id"] = result_device.get(ticket["result_id"])
            ticket["found_count"] = 1
            ticket["merged_result_ids"] = [ticket["result_id"]]
            ticket["last_found_at"] = ticket.get("closed_at") or ts
            ticket.setdefault("created_at", ts)
            if idx == 2:
                ticket["rectify_status"] = "CLOSED"
            else:
                ticket["rectify_status"] = "OPEN"
