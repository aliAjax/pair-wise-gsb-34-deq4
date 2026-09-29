export const mockData = {
  "building": [
    {
      "id": 1,
      "name": "name 1",
      "campus": "campus 1",
      "floor_count": "floor count 1",
      "fire_grade": "fire grade 1",
      "manager_id": 1,
      "address_code": "address code 1"
    },
    {
      "id": 2,
      "name": "name 2",
      "campus": "campus 2",
      "floor_count": "floor count 2",
      "fire_grade": "fire grade 2",
      "manager_id": 2,
      "address_code": "address code 2"
    },
    {
      "id": 3,
      "name": "name 3",
      "campus": "campus 3",
      "floor_count": "floor count 3",
      "fire_grade": "fire grade 3",
      "manager_id": 3,
      "address_code": "address code 3"
    }
  ],
  "fireDevice": [
    {
      "id": 1,
      "building_id": 1,
      "device_code": "device code 1",
      "device_type": "HYDRANT",
      "floor": "floor 1",
      "location_desc": "location desc 1",
      "install_date": "2026-06-11T09:00:00Z",
      "status": "IN_PROGRESS",
      "next_maintenance_at": "2026-06-11T09:00:00Z"
    },
    {
      "id": 2,
      "building_id": 2,
      "device_code": "device code 2",
      "device_type": "SMOKE_DETECTOR",
      "floor": "floor 2",
      "location_desc": "location desc 2",
      "install_date": "2026-06-12T09:00:00Z",
      "status": "SUBMITTED",
      "next_maintenance_at": "2026-06-12T09:00:00Z"
    },
    {
      "id": 3,
      "building_id": 3,
      "device_code": "device code 3",
      "device_type": "SPRINKLER",
      "floor": "floor 3",
      "location_desc": "location desc 3",
      "install_date": "2026-06-13T09:00:00Z",
      "status": "PLANNED",
      "next_maintenance_at": "2026-06-13T09:00:00Z"
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
      "checklist_version": "checklist version 1",
      "finished_at": "2026-06-11T09:00:00Z"
    },
    {
      "id": 2,
      "building_id": 2,
      "inspector_id": 2,
      "plan_date": "2026-06-12T09:00:00Z",
      "task_type": "SMOKE_DETECTOR",
      "status": "SUBMITTED",
      "checklist_version": "checklist version 2",
      "finished_at": "2026-06-12T09:00:00Z"
    },
    {
      "id": 3,
      "building_id": 3,
      "inspector_id": 3,
      "plan_date": "2026-06-13T09:00:00Z",
      "task_type": "SPRINKLER",
      "status": "PLANNED",
      "checklist_version": "checklist version 3",
      "finished_at": "2026-06-13T09:00:00Z"
    }
  ],
  "inspectionResult": [
    {
      "id": 1,
      "task_id": 1,
      "device_id": 1,
      "item_code": "item code 1",
      "result_status": "IN_PROGRESS",
      "measured_value": "measured value 1",
      "photo_url": "/mock/photo_url-1.png",
      "note": "note 1"
    },
    {
      "id": 2,
      "task_id": 2,
      "device_id": 2,
      "item_code": "item code 2",
      "result_status": "SUBMITTED",
      "measured_value": "measured value 2",
      "photo_url": "/mock/photo_url-2.png",
      "note": "note 2"
    },
    {
      "id": 3,
      "task_id": 3,
      "device_id": 3,
      "item_code": "item code 3",
      "result_status": "PLANNED",
      "measured_value": "measured value 3",
      "photo_url": "/mock/photo_url-3.png",
      "note": "note 3"
    }
  ],
  "hazardTicket": [
    {
      "id": 1,
      "result_id": 1,
      "severity": "severity 1",
      "owner_id": 1,
      "deadline": "deadline 1",
      "rectify_status": "OPEN",
      "rectify_note": "rectify note 1",
      "closed_at": "",
      "device_id": 1,
      "found_count": 2,
      "merged_result_ids": [1],
      "last_found_at": "2026-06-11T09:00:00Z"
    },
    {
      "id": 2,
      "result_id": 2,
      "severity": "severity 2",
      "owner_id": 2,
      "deadline": "deadline 2",
      "rectify_status": "OPEN",
      "rectify_note": "rectify note 2",
      "closed_at": "",
      "device_id": 2,
      "found_count": 1,
      "merged_result_ids": [2],
      "last_found_at": "2026-06-12T09:00:00Z"
    },
    {
      "id": 3,
      "result_id": 3,
      "severity": "severity 3",
      "owner_id": 3,
      "deadline": "deadline 3",
      "rectify_status": "CLOSED",
      "rectify_note": "rectify note 3",
      "closed_at": "2026-06-13T09:00:00Z",
      "device_id": 3,
      "found_count": 1,
      "merged_result_ids": [3],
      "last_found_at": "2026-06-13T09:00:00Z"
    }
  ],
  "checklistVersion": [
    {
      "id": 1,
      "task_type": "HYDRANT",
      "scope_key": "DEFAULT",
      "version": 1,
      "status": "PUBLISHED",
      "published_at": "2026-06-01T09:00:00Z",
      "published_by": 1,
      "created_at": "2026-06-01T09:00:00Z",
      "created_by": 1,
      "remark": "消火栓首版检查清单",
      "items": [
        {
          "item_code": "H_PRESSURE",
          "item_name": "管网压力(MPa)",
          "rule_type": "NUMERIC",
          "device_type": "HYDRANT",
          "severity": "HIGH",
          "min_value": 0.2,
          "max_value": 0.8,
          "critical_min": null,
          "critical_max": 1.0,
          "allowed_values": [],
          "abnormal_value": null,
          "required": true
        },
        {
          "item_code": "H_BOX",
          "item_name": "栓箱完好",
          "rule_type": "CHOICE",
          "device_type": "HYDRANT",
          "severity": "MEDIUM",
          "min_value": null,
          "max_value": null,
          "critical_min": null,
          "critical_max": null,
          "allowed_values": ["INTACT"],
          "abnormal_value": null,
          "required": true
        },
        {
          "item_code": "H_WATER",
          "item_name": "供水状态",
          "rule_type": "TEXT",
          "device_type": "HYDRANT",
          "severity": "HIGH",
          "min_value": null,
          "max_value": null,
          "critical_min": null,
          "critical_max": null,
          "allowed_values": [],
          "abnormal_value": "NO_WATER",
          "required": true
        }
      ]
    },
    {
      "id": 2,
      "task_type": "SMOKE_DETECTOR",
      "scope_key": "DEFAULT",
      "version": 1,
      "status": "PUBLISHED",
      "published_at": "2026-06-01T09:00:00Z",
      "published_by": 1,
      "created_at": "2026-06-01T09:00:00Z",
      "created_by": 1,
      "remark": "烟感首版检查清单",
      "items": [
        {
          "item_code": "SD_TEST",
          "item_name": "联动测试",
          "rule_type": "CHOICE",
          "device_type": "SMOKE_DETECTOR",
          "severity": "HIGH",
          "min_value": null,
          "max_value": null,
          "critical_min": null,
          "critical_max": null,
          "allowed_values": ["PASS"],
          "abnormal_value": null,
          "required": true
        }
      ]
    },
    {
      "id": 3,
      "task_type": "HYDRANT",
      "scope_key": "DEFAULT",
      "version": 2,
      "status": "DRAFT",
      "published_at": "",
      "published_by": null,
      "created_at": "2026-06-20T09:00:00Z",
      "created_by": 1,
      "remark": "消火栓清单改版（草稿）",
      "items": [
        {
          "item_code": "H_PRESSURE",
          "item_name": "管网压力(MPa)",
          "rule_type": "NUMERIC",
          "device_type": "HYDRANT",
          "severity": "CRITICAL",
          "min_value": 0.25,
          "max_value": 0.7,
          "critical_min": null,
          "critical_max": 0.9,
          "allowed_values": [],
          "abnormal_value": null,
          "required": true
        },
        {
          "item_code": "H_SEAL",
          "item_name": "铅封检查",
          "rule_type": "TEXT",
          "device_type": "HYDRANT",
          "severity": "MEDIUM",
          "min_value": null,
          "max_value": null,
          "critical_min": null,
          "critical_max": null,
          "allowed_values": [],
          "abnormal_value": "BROKEN",
          "required": true
        }
      ]
    }
  ]
} as const;
