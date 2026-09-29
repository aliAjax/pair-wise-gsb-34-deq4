import { useMemo } from "react";
import type { ChecklistItem } from "../types/ChecklistVersion";

export interface ChecklistValue {
  measured_value?: string;
  result_status?: string;
  judged_severity?: string;
}

// 按任务固定版本的检查项计算录入完成率与异常数，提交前在页面上实时展示
export function useChecklistProgress(items: ChecklistItem[] = [], values: Record<string, ChecklistValue> = {}) {
  return useMemo(() => {
    const total = items.length;
    const filled = items.filter((item) => (values[item.item_code]?.measured_value ?? "").trim() !== "").length;
    const abnormal = items.filter((item) => values[item.item_code]?.result_status === "ABNORMAL").length;
    const percent = total === 0 ? 0 : Math.round((filled / total) * 100);
    return { total, filled, abnormal, percent, completed: total > 0 && filled === total };
  }, [items, values]);
}
