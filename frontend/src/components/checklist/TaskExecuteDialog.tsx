import { useMemo, useState } from "react";
import { listFireDevice } from "../../api/FireDevice";
import { ChecklistPanel } from "../common/ChecklistPanel";
import { useChecklistProgress } from "../../hooks/useChecklistProgress";
import { createInspectionEntry } from "../../constructors/InspectionTaskConstructor";
import { useInspectionTaskStore } from "../../stores/InspectionTaskStore";
import type { ChecklistValue } from "../../hooks/useChecklistProgress";
import type { FireDevice } from "../../types/FireDevice";
import type { InspectionSubmitResult, InspectionTask } from "../../types/InspectionTask";
import { useAsyncOnce } from "../../hooks/useAsyncOnce";
import { HazardSeverityTag } from "../common/HazardSeverityTag";

export function TaskExecuteDialog({ task, onClose }: { task: InspectionTask; onClose: () => void }) {
  const submit = useInspectionTaskStore((state) => state.submit);
  const [values, setValues] = useState<Record<string, ChecklistValue>>({});
  const [deviceMap, setDeviceMap] = useState<Record<string, number>>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<InspectionSubmitResult | null>(null);

  const items = task.pinned_items ?? [];
  const progress = useChecklistProgress(items, values);

  useAsyncOnce(() => listFireDevice().then((rows: FireDevice[]) => {
    const sameType = rows.filter((device) => device.device_type === task.task_type);
    const initial: Record<string, number> = {};
    items.forEach((item, index) => {
      initial[item.item_code] = sameType[index % Math.max(sameType.length, 1)]?.id ?? rows[0]?.id ?? 1;
    });
    setDeviceMap(initial);
  }), [items.length, task.task_type]);

  const pinnedVersion = useMemo(
    () => ({ version: task.version_no ?? 1, status: "PUBLISHED" as const, remark: `任务固定版本：${task.checklist_version}` }),
    [task.checklist_version, task.version_no]
  );

  const handleChange = (itemCode: string, measured_value: string) => {
    setValues((previous) => ({ ...previous, [itemCode]: { ...previous[itemCode], measured_value } }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError("");
    try {
      const entries = items.map((item) =>
        createInspectionEntry(item, deviceMap[item.item_code] ?? 1, {
          measured_value: values[item.item_code]?.measured_value ?? ""
        })
      );
      const submitted = await submit(task.id, { entries });
      const graded: Record<string, ChecklistValue> = {};
      submitted.results.forEach((row) => {
        graded[row.item_code] = {
          measured_value: row.measured_value,
          result_status: row.result_status,
          judged_severity: row.judged_severity
        };
      });
      setValues(graded);
      setResult(submitted);
    } catch (err) {
      setError(err instanceof Error ? err.message : "提交失败");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-mask" onClick={onClose}>
      <div className="modal wide" onClick={(event) => event.stopPropagation()}>
        <div className="panel-head">
          <h2>执行任务 #{task.id}</h2>
          <span className="muted">
            {task.task_type} · 按建任务时固定的 {task.checklist_version} 判级
          </span>
        </div>
        {task.version_notice ? <p className="notice">建任务提示：{task.version_notice}</p> : null}

        <ChecklistPanel version={pinnedVersion} items={items} values={values} editable={!result} onChange={handleChange} />

        {!result ? (
          <p className="muted">
            已录入 {progress.filled}/{progress.total}（{progress.percent}%），异常 {progress.abnormal} 项
          </p>
        ) : null}

        {result ? (
          <div className="submit-summary">
            <h3>提交完成</h3>
            <p>
              异常 <strong>{result.abnormal_count}</strong> 项 · 新开隐患单{" "}
              <strong>{result.created_tickets.length}</strong> 张 · 并入未关闭隐患{" "}
              <strong>{result.merged_tickets.length}</strong> 次
            </p>
            {[...result.created_tickets, ...result.merged_tickets].length > 0 ? (
              <ul className="ticket-flash">
                {result.created_tickets.map((ticket) => (
                  <li key={`new-${(ticket as { id: number }).id}`}>
                    新开隐患单 #{(ticket as { id: number }).id}
                    <HazardSeverityTag value={(ticket as { severity: string }).severity} />
                    <span className="muted">发现次数 {(ticket as { found_count: number }).found_count}</span>
                  </li>
                ))}
                {result.merged_tickets.map((ticket) => (
                  <li key={`merged-${(ticket as { id: number }).id}`}>
                    已合并到隐患单 #{(ticket as { id: number }).id}
                    <HazardSeverityTag value={(ticket as { severity: string }).severity} />
                    <span className="muted">累计发现 {(ticket as { found_count: number }).found_count} 次</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted">本次无异常，未生成隐患单。</p>
            )}
          </div>
        ) : null}

        {error ? <p className="error">{error}</p> : null}
        <div className="modal-actions">
          <button type="button" onClick={onClose}>
            {result ? "关闭" : "取消"}
          </button>
          {!result ? (
            <button type="button" className="primary" disabled={submitting || !progress.completed} onClick={handleSubmit}>
              {submitting ? "提交中…" : "按固定版本提交"}
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
