// 本地种子数据（离线评审用），接口可用时以前后端 /api 返回为准。
// 任务带固定版本快照，结果带判级结论，隐患单带发现次数，与后端结构保持一致。
export const mockData = {
  "building": [
    {
      "id": 1,
      "name": "1 号研发楼",
      "campus": "南区科技园",
      "floor_count": "8",
      "fire_grade": "一级",
      "manager_id": 1,
      "address_code": "440300"
    }
  ],
  "fireDevice": [
    {
      "id": 1,
      "building_id": 1,
      "device_code": "HYD-0001",
      "device_type": "HYDRANT",
      "floor": "1F",
      "location_desc": "大堂东侧消火栓",
      "install_date": "2026-06-11T09:00:00Z",
      "status": "IN_SERVICE",
      "next_maintenance_at": "2026-12-11T09:00:00Z"
    }
  ],
  "inspectionTask": [
    {
      "id": 1,
      "building_id": 1,
      "inspector_id": 1,
      "plan_date": "2026-06-11T09:00:00Z",
      "task_type": "HYDRANT",
      "status": "IN_PROGRESS",
      "checklist_version": "1.0.0",
      "checklist_version_id": 1,
      "version_pinned_at": "2026-06-01T09:00:00Z",
      "created_by": 1,
      "version_notice": "",
      "finished_at": "",
      "checklist_snapshot": [
        {
          "item_code": "HYD-PRESSURE",
          "item_name": "栓口静水压力",
          "device_type": "HYDRANT",
          "rule": { "kind": "threshold", "min": 0.15, "max": 1.0, "unit": "MPa" },
          "fail_severity": "HIGH"
        }
      ]
    }
  ],
  "inspectionResult": [
    {
      "id": 1,
      "task_id": 1,
      "device_id": 1,
      "item_code": "HYD-PRESSURE",
      "result_status": "DONE",
      "measured_value": "0.20",
      "photo_url": "",
      "note": "",
      "outcome": "NORMAL",
      "checklist_version": "1.0.0",
      "graded_at": "2026-06-11T10:00:00Z"
    }
  ],
  "hazardTicket": [
    {
      "id": 1,
      "result_id": 1,
      "first_result_id": 1,
      "latest_result_id": 1,
      "device_id": null,
      "severity": "HIGH",
      "owner_id": 1,
      "deadline": "",
      "rectify_status": "OPEN",
      "rectify_note": "",
      "closed_at": "",
      "found_count": 1,
      "created_at": "2026-06-11T10:00:00Z",
      "updated_at": "2026-06-11T10:00:00Z"
    }
  ],
  "checklistVersion": [
    {
      "id": 1,
      "task_type": "HYDRANT",
      "version": "1.0.0",
      "status": "PUBLISHED",
      "remark": "首版消火栓巡检清单",
      "created_by": 1,
      "published_by": 1,
      "created_at": "2026-06-01T09:00:00Z",
      "published_at": "2026-06-01T09:00:00Z",
      "items": []
    }
  ]
} as const;
