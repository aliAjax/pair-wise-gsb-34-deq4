def create_checklist_item_dto(**overrides):
    row = {
        "item_code": "ITEM-001",
        "item_name": "检查项",
        "device_type": None,
        "rule": {"kind": "options", "normal": ["NORMAL", "YES"]},
        "fail_severity": "MEDIUM",
    }
    row.update(overrides)
    return row


def create_checklist_version_dto(**overrides):
    row = {
        "id": 1,
        "task_type": "HYDRANT",
        "version": "1.0.0",
        "status": "DRAFT",
        "remark": "",
        "created_by": 1,
        "published_by": None,
        "created_at": "2026-06-01T09:00:00Z",
        "published_at": None,
        "items": [],
    }
    row.update(overrides)
    return row
