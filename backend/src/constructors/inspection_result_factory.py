def create_inspection_result_dto(**overrides):
    row = {
        "id": 1,
        "task_id": 1,
        "device_id": 1,
        "item_code": "item code 1",
        "result_status": "IN_PROGRESS",
        "measured_value": "measured value 1",
        "photo_url": "/mock/photo_url-1.png",
        "note": "note 1",
        # 按任务固定版本判级后写入的结论与版本号，便于追溯
        "outcome": "",
        "checklist_version": "",
        "graded_at": "",
    }
    row.update(overrides)
    return row
