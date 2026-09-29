def create_inspection_task_dto(**overrides):
    row = {
        "id": 1,
        "building_id": 1,
        "inspector_id": 1,
        "plan_date": "2026-06-11T09:00:00Z",
        "task_type": "HYDRANT",
        "status": "PLANNED",
        "checklist_version": "v1",
        "checklist_version_id": 1,
        "version_no": 1,
        "pinned_items": [],
        "finished_at": "",
        "created_at": "",
        "created_by": 1,
        "version_notice": "",
    }
    row.update(overrides)
    return row
