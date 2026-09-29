export const ChecklistRuleType = ["NUMERIC", "CHOICE", "TEXT"] as const;
export type ChecklistRuleType = (typeof ChecklistRuleType)[number];
export const ChecklistRuleTypeText: Record<ChecklistRuleType, string> = {
  NUMERIC: "数值区间",
  CHOICE: "选项判定",
  TEXT: "文本标记"
};

export const ChecklistPublishStatus = ["DRAFT", "PUBLISHED"] as const;
export type ChecklistPublishStatus = (typeof ChecklistPublishStatus)[number];
export const ChecklistPublishStatusText: Record<ChecklistPublishStatus, string> = {
  DRAFT: "草稿",
  PUBLISHED: "已发布"
};

// 建任务与发布并发时的提示类型
export const VersionNoticeKind = ["NONE", "PUBLISHED_DURING_CREATE", "PUBLISHED_JUST_NOW"] as const;
export type VersionNoticeKind = (typeof VersionNoticeKind)[number];
