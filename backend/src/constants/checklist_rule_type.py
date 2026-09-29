# 清单判定规则类型：
# NUMERIC  数值型，按 min/max 判级，超 critical_min/critical_max 升为 CRITICAL
# CHOICE   选项型，measured_value 必须命中 allowed_values，否则按 item.severity 判异常
# TEXT     文本型，measured_value == abnormal_value（默认 ABNORMAL）即异常
ChecklistRuleType = ["NUMERIC", "CHOICE", "TEXT"]

# 清单发布状态：草稿仅可编辑，已发布版本被任务快照引用、永久不可变
ChecklistPublishStatus = ["DRAFT", "PUBLISHED"]
