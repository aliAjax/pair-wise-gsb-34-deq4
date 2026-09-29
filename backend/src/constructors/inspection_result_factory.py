def create_inspection_result_dto(**overrides):
    row = {
        "id": 1,
        "task_id": 1,
        "device_id": 1,
        "item_code": "H_PRESSURE",
        "result_status": "PENDING",
        "judged_severity": "",
        "checklist_version": "v1",
        "measured_value": "",
        "photo_url": "",
        "note": "",
        "submitted_at": "",
    }
    row.update(overrides)
    return row
