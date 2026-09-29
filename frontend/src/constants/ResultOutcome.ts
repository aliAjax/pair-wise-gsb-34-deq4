export const ResultOutcome = ["NORMAL", "ABNORMAL", "NOT_CHECKED"] as const;
export type ResultOutcome = (typeof ResultOutcome)[number];
export const ResultOutcomeText: Record<ResultOutcome, string> = {
  NORMAL: "正常",
  ABNORMAL: "异常",
  NOT_CHECKED: "未检查"
};
