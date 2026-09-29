import { useMemo, useState } from "react";
import type { ChecklistItem } from "../types/ChecklistVersion";

export interface ChecklistProgressRow {
  item: ChecklistItem;
  measuredValue: string;
  done: boolean;
}

/**
 * 基于任务固定版本快照计算检查项填写进度。
 * 快照在建任务时冻结，因此清单后续发布不会改变这里的检查项集合。
 */
export function useChecklistProgress(snapshot: ChecklistItem[] = []) {
  const [values, setValues] = useState<Record<string, string>>({});

  const rows: ChecklistProgressRow[] = useMemo(() => snapshot.map((item) => {
    const measuredValue = values[item.item_code] ?? "";
    return { item, measuredValue, done: measuredValue.trim().length > 0 };
  }), [snapshot, values]);

  const checkedCount = rows.filter((row) => row.done).length;
  const total = rows.length;
  const percent = total === 0 ? 0 : Math.round((checkedCount / total) * 100);

  const setMeasuredValue = (itemCode: string, measuredValue: string) => {
    setValues((prev) => ({ ...prev, [itemCode]: measuredValue }));
  };

  return { rows, values, checkedCount, total, percent, setMeasuredValue };
}
