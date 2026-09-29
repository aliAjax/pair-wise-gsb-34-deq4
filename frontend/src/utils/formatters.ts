import type { ChecklistItem, ChecklistRule } from "../types/ChecklistVersion";

export const formatDate = (value: string) => (value ? new Date(value).toLocaleString("zh-CN") : "—");
export const formatStatus = (value: string) => value.replace(/_/g, " ");
export const formatNumber = (value: number) => new Intl.NumberFormat("zh-CN").format(value);
export const formatRisk = (value: string) => ({ LOW: "低", MEDIUM: "中", HIGH: "高", CRITICAL: "严重", EXTREME: "极高" }[value] ?? value);

export const formatVersion = (value: string) => (value ? `v${value}` : "未固定版本");

export const formatRule = (rule: ChecklistRule): string => {
  if (rule.kind === "threshold") {
    const range = [rule.min != null ? `≥${rule.min}` : "", rule.max != null ? `≤${rule.max}` : ""]
      .filter(Boolean)
      .join(" 且 ");
    return range ? `数值${range}${rule.unit ? ` ${rule.unit}` : ""}` : "数值阈值";
  }
  if (rule.kind === "presence") {
    return rule.must === false ? "应为空" : "必须有值";
  }
  const normal = (rule.normal ?? []).join("/");
  return normal ? `取值 ${normal} 判正常` : "选择项判定";
};

export const summarizeChecklist = (items: ChecklistItem[]): string =>
  items.map((item) => `${item.item_code}（${formatRule(item.rule)}）`).join("；");
