export const ChecklistStatus = ["DRAFT", "PUBLISHED", "ARCHIVED"] as const;
export type ChecklistStatus = (typeof ChecklistStatus)[number];
export const ChecklistStatusText: Record<ChecklistStatus, string> = {
  DRAFT: "草稿",
  PUBLISHED: "已发布",
  ARCHIVED: "已归档"
};
