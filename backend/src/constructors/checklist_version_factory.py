def create_checklist_item_dto(**overrides):
    row = {
        "item_code": "ITEM_CODE",
        "item_name": "检查项",
        "rule_type": "TEXT",
        "device_type": "HYDRANT",
        "severity": "MEDIUM",
        "min_value": None,
        "max_value": None,
        "critical_min": None,
        "critical_max": None,
        "allowed_values": [],
        "abnormal_value": "ABNORMAL",
        "required": True,
    }
    row.update(overrides)
    return row


def create_checklist_version_dto(**overrides):
    row = {
        "id": 1,
        "task_type": "HYDRANT",
        "scope_key": "DEFAULT",
        "version": 1,
        "status": "DRAFT",
        "items": [],
        "published_at": "",
        "published_by": None,
        "created_at": "",
        "created_by": None,
        "remark": "",
    }
    row.update(overrides)
    return row
