export const ERROR_MESSAGES = {
  AUTH_REQUIRED: "请先登录后再继续操作",
  RBAC_DENIED: "当前角色没有执行该动作的权限",
  VALIDATION_FAILED: "表单字段缺失或格式错误",
  RATE_LIMITED: "请求过于频繁，请稍后再试",
  CHECKLIST_NOT_FOUND: "巡检清单版本不存在",
  CHECKLIST_NOT_PUBLISHABLE: "只有草稿状态的清单才能发布",
  CHECKLIST_NO_PUBLISHED_VERSION: "该任务类型暂无已发布清单，无法创建任务",
  CHECKLIST_ITEM_CODE_CONFLICT: "清单内存在重复的检查项编号或版本号",
  TASK_NOT_FOUND: "巡检任务不存在",
  TASK_NOT_SUBMITTABLE: "当前任务状态不允许提交（可能已提交）",
  TASK_CHECKLIST_VERSION_MISSING: "任务缺少固定清单版本，无法判级",
  RESULT_ITEM_UNKNOWN: "提交的检查项不属于任务固定版本，已拒绝按新规则判级",
  HAZARD_NOT_FOUND: "隐患整改单不存在",
  HAZARD_ALREADY_CLOSED: "隐患整改单已关闭，不能重复关闭"
} as const;
