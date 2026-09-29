import { ChecklistRuleTypeText } from "../constants/ChecklistVersion";
import { RectifyStatusText } from "../constants/RectifyStatus";
import { ResultStatusText } from "../constants/ResultStatus";

export const formatDate = (value: string) => new Date(value).toLocaleString("zh-CN");
export const formatStatus = (value: string) => value.replace(/_/g, " ");
export const formatNumber = (value: number) => new Intl.NumberFormat("zh-CN").format(value);
export const formatRisk = (value: string) =>
  ({ LOW: "低", MEDIUM: "中", HIGH: "高", CRITICAL: "严重", EXTREME: "极高", NORMAL: "正常" } as Record<string, string>)[
    value
  ] ?? value;
export const formatResultStatus = (value: string) => ResultStatusText[value as keyof typeof ResultStatusText] ?? value;
export const formatRectifyStatus = (value: string) =>
  RectifyStatusText[value as keyof typeof RectifyStatusText] ?? value;
export const formatRuleType = (value: string) =>
  ChecklistRuleTypeText[value as keyof typeof ChecklistRuleTypeText] ?? value;
// 任务上展示的固定版本标签：优先 vN，回退后端历史字符串
export const formatChecklistVersion = (label?: string, versionNo?: number) =>
  label || (versionNo ? `v${versionNo}` : "-");
