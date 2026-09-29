def create_hazard_ticket_dto(**overrides):
    row = {
        "id": 1,
        "result_id": 1,
        "device_id": 1,
        "severity": "MEDIUM",
        "owner_id": 1,
        "deadline": "deadline 1",
        "rectify_status": "OPEN",
        "rectify_note": "rectify note 1",
        "closed_at": "",
        # 发现次数：同一设备存在未关闭隐患时，新异常合并到原单并累计
        "found_count": 1,
        "first_result_id": 1,
        "latest_result_id": 1,
        "created_at": "2026-06-11T09:00:00Z",
        "updated_at": "2026-06-11T09:00:00Z",
    }
    row.update(overrides)
    return row
