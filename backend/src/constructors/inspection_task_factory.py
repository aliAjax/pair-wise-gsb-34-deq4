def create_inspection_task_dto(**overrides):
    row = {
        "id": 1,
        "building_id": 1,
        "inspector_id": 1,
        "plan_date": "2026-06-11T09:00:00Z",
        "task_type": "HYDRANT",
        "status": "PLANNED",
        # 建任务时固定的清单版本：执行期间不随后续发布而变化
        "checklist_version": "1.0.0",
        "checklist_version_id": 1,
        "version_pinned_at": "2026-06-01T09:00:00Z",
        "created_by": 1,
        "version_notice": "",
        "finished_at": "",
    }
    row.update(overrides)
    return row


def create_task_snapshot_item_dto(**overrides):
    """任务固定时刻冻结的检查项快照（判级的权威依据）。"""
    row = {
        "item_code": "ITEM-001",
        "item_name": "检查项",
        "device_type": None,
        "rule": {"kind": "options", "normal": ["NORMAL", "YES"]},
        "fail_severity": "MEDIUM",
    }
    row.update(overrides)
    return row
