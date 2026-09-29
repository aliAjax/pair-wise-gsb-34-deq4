LOG_TEMPLATES = {
  "Building": [
    "Building.create",
    "Building.update",
    "Building.status",
    "Building.export"
  ],
  "FireDevice": [
    "FireDevice.create",
    "FireDevice.update",
    "FireDevice.status",
    "FireDevice.export"
  ],
  "InspectionTask": [
    "InspectionTask.create",
    "InspectionTask.update",
    "InspectionTask.status",
    "InspectionTask.export",
    # 建任务时固定清单版本（含发布并发提示）、提交按快照版本判级
    "InspectionTask.create.pinned_checklist",
    "InspectionTask.submit"
  ],
  "InspectionResult": [
    "InspectionResult.create",
    "InspectionResult.update",
    "InspectionResult.status",
    "InspectionResult.export"
  ],
  "HazardTicket": [
    "HazardTicket.create",
    "HazardTicket.update",
    "HazardTicket.status",
    "HazardTicket.export",
    # 同设备未关闭隐患合并并累计发现次数
    "HazardTicket.merge"
  ],
  "ChecklistVersion": [
    # 清单草稿创建、发布（旧任务不受影响）、发布与建任务并发、版本查询
    "ChecklistVersion.create",
    "ChecklistVersion.publish",
    "ChecklistVersion.publish_concurrent",
    "ChecklistVersion.export"
  ]
}
