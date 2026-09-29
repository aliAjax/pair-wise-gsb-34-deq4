export const ResultStatus = ["PENDING", "NORMAL", "ABNORMAL"] as const;
export type ResultStatus = (typeof ResultStatus)[number];
export const ResultStatusText: Record<ResultStatus, string> = {
  PENDING: "待判定",
  NORMAL: "正常",
  ABNORMAL: "异常"
};
