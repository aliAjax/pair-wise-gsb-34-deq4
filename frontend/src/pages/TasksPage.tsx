import { useEffect, useMemo, useState } from "react";
import { ChecklistPanel } from "../components/common/ChecklistPanel";
import { StatusBadge } from "../components/common/StatusBadge";
import { TimelineList, type TimelineEntry } from "../components/common/TimelineList";
import { HazardSeverityTag } from "../components/common/HazardSeverityTag";
import { useChecklistProgress } from "../hooks/useChecklistProgress";
import { useHazardFlow } from "../hooks/useHazardFlow";
import { useInspectionTaskStore } from "../stores/InspectionTaskStore";
import { useChecklistVersionStore } from "../stores/ChecklistVersionStore";
import { listAuditLog } from "../api/AuditLog";
import type { AuditLog } from "../types/AuditLog";
import type { ChecklistItemInput } from "../types/ChecklistVersion";
import type { InspectionTask } from "../types/InspectionTask";
import { formatDate, formatVersion } from "../utils/formatters";

const DEVICE_BY_DEFAULT = 1;

function TaskExecutor({ task }: { task: InspectionTask }) {
  const progress = useChecklistProgress(task.checklist_snapshot);
  const flow = useHazardFlow();

  const handleSubmit = async () => {
    const results: ChecklistItemInput[] = progress.rows
      .filter((row) => row.done)
      .map((row) => ({
        item_code: row.item.item_code,
        measured_value: row.measuredValue,
        device_id: DEVICE_BY_DEFAULT
      }));
    await flow.submit(task.id, results);
  };

  const submittable = task.status === "PLANNED" || task.status === "IN_PROGRESS";

  return (
    <article className="panel task-card">
      <header className="task-card-head">
        <div>
          <h3>任务 #{task.id} · {task.task_type}</h3>
          <p className="muted">
            楼栋 {task.building_id} · 巡检员 {task.inspector_id} · 计划 {formatDate(task.plan_date)}
          </p>
        </div>
        <StatusBadge value={task.status} />
      </header>

      <p className="version-line">
        建任务时固定版本：<strong>{formatVersion(task.checklist_version)}</strong>
        <span className="muted">（固定于 {formatDate(task.version_pinned_at)}）</span>
      </p>
      {task.version_notice ? (
        <p className="notice" role="status">⚠️ {task.version_notice}</p>
      ) : null}

      <ChecklistPanel
        version={task.checklist_version}
        items={task.checklist_snapshot}
        values={progress.values}
        onValueChange={progress.setMeasuredValue}
        readonly={!submittable}
      />

      {submittable ? (
        <div className="task-actions">
          <span className="muted">填写进度 {progress.checkedCount}/{progress.total}（{progress.percent}%）</span>
          <button type="button" disabled={flow.submitting} onClick={handleSubmit}>
            {submittingLabel(flow.submitting)}
          </button>
        </div>
      ) : (
        <p className="muted">任务已于 {formatDate(task.finished_at)} 按固定版本提交，后续清单发布不影响其判级。</p>
      )}

      {flow.error ? <p className="error">{flow.error}</p> : null}
      {flow.lastResponse ? (
        <section className="submit-result">
          <h4>提交结果（按 {formatVersion(flow.lastResponse.task.checklist_version)} 判级）</h4>
          <ul>
            {flow.lastResponse.results.map((result) => {
              const sourceItem = task.checklist_snapshot.find((item) => item.item_code === result.item_code);
              return (
                <li key={result.id} className={`outcome outcome-${result.outcome.toLowerCase()}`}>
                  {result.item_code}：{result.outcome}
                  {result.outcome === "ABNORMAL" && sourceItem?.fail_severity
                    ? <HazardSeverityTag value={sourceItem.fail_severity} />
                    : null}
                </li>
              );
            })}
          </ul>
          {flow.lastResponse.hazard_tickets.length > 0 ? (
            <p className="notice">
              异常项已生成/合并隐患单：
              {flow.lastResponse.hazard_tickets.map((ticket) =>
                `#${ticket.id}(发现 ${ticket.found_count} 次)`).join("，")}
            </p>
          ) : (
            <p className="muted">本次无异常项，未生成隐患单。</p>
          )}
        </section>
      ) : null}
    </article>
  );
}

function submittingLabel(submitting: boolean): string {
  return submitting ? "提交中…" : "按固定版本提交";
}

export function TasksPage() {
  const taskStore = useInspectionTaskStore();
  const checklistStore = useChecklistVersionStore();
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    taskStore.load();
    checklistStore.load();
    listAuditLog({ targetType: "InspectionTask" }).then(setLogs).catch(() => setLogs([]));
  }, []);

  const timeline: TimelineEntry[] = useMemo(() => logs.slice(0, 10).map((log) => ({
    id: log.id,
    title: log.action,
    description: log.detail ? JSON.stringify(log.detail) : "",
    at: formatDate(log.created_at),
    tone: log.action.includes("submit") ? "abnormal" : ""
  })), [logs]);

  const refreshLogs = () => listAuditLog({ targetType: "InspectionTask" }).then(setLogs);

  const handlePublish = async (versionId: number) => {
    await checklistStore.publish(versionId);
    await taskStore.load();
    refreshLogs();
  };

  const handleCreate = async () => {
    try {
      await taskStore.create({
        building_id: 1,
        inspector_id: 1,
        plan_date: new Date().toISOString(),
        task_type: "HYDRANT",
        created_by: 1
      });
      refreshLogs();
    } catch {
      // 错误提示由 store 调用方扩展，当前页面保留固定版本演示入口
    }
  };

  return (
    <section className="page-stack">
      <div className="panel">
        <h2>巡检清单发布（物业）</h2>
        <p className="muted">发布后只影响此后新建的任务；已领取任务继续按其固定版本执行与判级。</p>
        <div className="table">
          {checklistStore.rows.map((version) => (
            <article key={version.id} className="row checklist-row">
              <strong>{version.task_type} {formatVersion(version.version)}</strong>
              <StatusBadge value={version.status} />
              <span className="muted">{version.items.length} 项</span>
              <span className="muted">
                {version.status === "PUBLISHED" ? `发布于 ${formatDate(version.published_at ?? "")}` : "未发布"}
              </span>
              {version.status === "DRAFT" ? (
                <button type="button" onClick={() => handlePublish(version.id)}>发布此版本</button>
              ) : null}
            </article>
          ))}
        </div>
        <div className="task-actions">
          <button type="button" onClick={handleCreate}>新建消火栓巡检任务（固定当前已发布版本）</button>
          {taskStore.lastNotice ? <span className="notice" role="status">{taskStore.lastNotice}</span> : null}
        </div>
      </div>

      <div className="panel">
        <h2>巡检任务</h2>
        {taskStore.loading ? <p className="muted">加载中…</p> : (
          <div className="task-grid">
            {taskStore.rows.filter((task) => task.task_type === "HYDRANT").map((task) => (
              <TaskExecutor key={task.id} task={task} />
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <h2>任务追溯</h2>
        <TimelineList entries={timeline} />
      </div>
    </section>
  );
}
