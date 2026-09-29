export const ERROR_MESSAGES = {
  AUTH_REQUIRED: "请先登录后再继续操作",
  RBAC_DENIED: "当前角色没有执行该动作的权限",
  VALIDATION_FAILED: "表单字段缺失或格式错误",
  RATE_LIMITED: "请求过于频繁，请稍后再试",
  CHECKLIST_NOT_FOUND: "清单版本不存在",
  CHECKLIST_NOT_PUBLISHED: "该设备类型还没有已发布清单",
  CHECKLIST_ALREADY_PUBLISHED: "清单已发布，发布后不可变更",
  CHECKLIST_VERSION_CONFLICT: "创建任务期间清单已更新",
  CHECKLIST_ITEM_NOT_FOUND: "提交项不属于任务固定的清单版本",
  TASK_NOT_FOUND: "巡检任务不存在",
  TASK_ALREADY_SUBMITTED: "任务已提交，不能重复提交"
};
