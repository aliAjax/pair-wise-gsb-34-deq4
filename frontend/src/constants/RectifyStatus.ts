export const RectifyStatus = ["OPEN", "CLOSED"] as const;
export type RectifyStatus = (typeof RectifyStatus)[number];
export const RectifyStatusText: Record<RectifyStatus, string> = {
  OPEN: "未关闭",
  CLOSED: "已关闭"
};
