export const HazardRectifyStatus = ["OPEN", "RECTIFYING", "REVIEWING", "CLOSED"] as const;
export type HazardRectifyStatus = (typeof HazardRectifyStatus)[number];
export const HazardRectifyStatusText: Record<HazardRectifyStatus, string> = {
  OPEN: "待整改",
  RECTIFYING: "整改中",
  REVIEWING: "待复验",
  CLOSED: "已关闭"
};
export const HAZARD_OPEN_STATUSES: HazardRectifyStatus[] = ["OPEN", "RECTIFYING", "REVIEWING"];
