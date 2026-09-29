ERROR_MESSAGES = {
    "AUTH_REQUIRED": "missing token",
    "RBAC_DENIED": "role denied",
    "VALIDATION_FAILED": "invalid payload",
    # 清单版本化
    "CHECKLIST_NOT_FOUND": "checklist {checklist_id} not found",
    "CHECKLIST_NOT_PUBLISHABLE": "only DRAFT checklist can be published, current status: {status}",
    "CHECKLIST_NO_PUBLISHED_VERSION": "no published checklist version available for task_type {task_type}",
    "CHECKLIST_ITEM_CODE_CONFLICT": "item_code {item_code} duplicated in checklist version {version}",
    # 任务提交
    "TASK_NOT_FOUND": "inspection task {task_id} not found",
    "TASK_NOT_SUBMITTABLE": "task {task_id} is {status}, only PLANNED/IN_PROGRESS tasks accept submission",
    "TASK_CHECKLIST_VERSION_MISSING": "task {task_id} has no pinned checklist version, cannot grade results",
    "RESULT_ITEM_UNKNOWN": "item_code {item_code} is not part of checklist {version} pinned by task {task_id}",
    # 隐患合并
    "HAZARD_NOT_FOUND": "hazard ticket {ticket_id} not found",
    "HAZARD_ALREADY_CLOSED": "hazard ticket {ticket_id} already closed",
}
