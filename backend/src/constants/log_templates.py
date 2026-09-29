# 写操作日志模板：每个实体至少 4 条，service 层写操作必须记录。
# 字段变更时需要同步修改这里与对应 service 调用处。
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
    # 版本固定与完成
    "InspectionTask.pin_checklist",
    "InspectionTask.submit",
    "InspectionTask.review"
  ],
  "InspectionResult": [
    "InspectionResult.create",
    "InspectionResult.update",
    "InspectionResult.status",
    "InspectionResult.export",
    # 按固定版本判级
    "InspectionResult.grade"
  ],
  "HazardTicket": [
    "HazardTicket.create",
    "HazardTicket.update",
    "HazardTicket.status",
    "HazardTicket.export",
    # 同设备未关闭隐患合并并累计发现次数
    "HazardTicket.merge",
    "HazardTicket.close"
  ],
  "ChecklistVersion": [
    "ChecklistVersion.create",
    "ChecklistVersion.update",
    "ChecklistVersion.publish",
    "ChecklistVersion.archive"
  ]
}
