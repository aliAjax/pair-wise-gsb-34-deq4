def create_hazard_ticket_dto(**overrides):
    row = {
        "id": 1,
        "result_id": 1,
        "device_id": 1,
        "severity": "MEDIUM",
        "owner_id": 1,
        "deadline": "",
        "rectify_status": "OPEN",
        "rectify_note": "",
        "closed_at": "",
        "found_count": 1,
        "merged_result_ids": [1],
        "last_found_at": "",
        "created_at": "",
    }
    row.update(overrides)
    return row
