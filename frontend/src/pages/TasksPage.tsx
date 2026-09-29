import { useEffect, useState } from "react";
import { ChecklistPublishPanel } from "../components/checklist/ChecklistPublishPanel";
import { TaskCreateDialog } from "../components/checklist/TaskCreateDialog";
import { TaskExecuteDialog } from "../components/checklist/TaskExecuteDialog";
import { StatusBadge } from "../components/common/StatusBadge";
import { TimelineList } from "../components/common/TimelineList";
import { DeviceTypeText } from "../constants/DeviceType";
import { listAuditLog } from "../api/AuditLog";
import { useInspectionTaskStore } from "../stores/InspectionTaskStore";
import type { AuditLog } from "../types/AuditLog";
import type { InspectionTask } from "../types/InspectionTask";

export function TasksPage() {
  const { rows, loading, load, lastVersionNotice, clearNotice } = useInspectionTaskStore();
  const [creating, setCreating] = useState(false);
  const [executing, setExecuting] = useState<InspectionTask | null>(null);
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    void listAuditLog().then((all) =>
      setLogs(
        all
          .filter((log) => ["ChecklistVersion", "InspectionTask"].includes(log.target_type))
          .slice(-12)
          .reverse()
      )
    );
  }, [creating, executing, rows.length]);

  const refreshLogs = () =>
    listAuditLog().then((all) =>
      setLogs(
        all
          .filter((log) => ["ChecklistVersion", "InspectionTask"].includes(log.target_type))
          .slice(-12)
          .reverse()
      )
    );

  return (
    <section className="page">
      <header className="page-head">
        <div>
          <p className="eyebrow">fire-inspect</p>
          <h1>巡检任务</h1>
          <p className="muted">建任务时固定当时已发布清单版本；提交按该版本判级，异常自动生成/合并隐患单。</p>
        </div>
        <button type="button" className="primary" onClick={() => setCreating(true)}>
          创建巡检任务
        </button>
      </header>

      {lastVersionNotice ? (
        <div className="notice-bar" role="alert">
          <span>{lastVersionNotice}</span>
          <button type="button" onClick={clearNotice}>
            我知道了
          </button>
        </div>
      ) : null}

      <div className="workbench tasks-layout">
        <div className="panel wide">
          <h2>任务列表（固定版本）</h2>
          {loading ? <p className="muted">加载中…</p> : null}
          <div className="table">
            {rows.map((task) => (
              <article key={task.id} className="row task-row">
                <div>
                  <strong>
                    任务 #{task.id} · {DeviceTypeText[task.task_type as keyof typeof DeviceTypeText] ?? task.task_type}
                  </strong>
                  <span className="muted">
                    {" "}
                    楼栋 {task.building_id} · 检查项 {task.pinned_items?.length ?? 0} 项
                  </span>
                </div>
                <span className="version-chip">固定 {task.checklist_version || "v?"}</span>
                <StatusBadge value={task.status} />
                <button
                  type="button"
                  disabled={task.status === "SUBMITTED" || task.status === "REVIEWED"}
                  onClick={() => setExecuting(task)}
                >
                  {task.status === "SUBMITTED" ? "已提交" : "执行/提交"}
                </button>
              </article>
            ))}
          </div>
        </div>
        <TimelineList
          title="发布与任务追溯"
          entries={logs.map((log) => ({
            id: log.id,
            action: log.action,
            actor: log.actor,
            detail: log.detail,
            created_at: log.created_at
          }))}
        />
      </div>

      <ChecklistPublishPanel onPublished={refreshLogs} />

      {creating ? <TaskCreateDialog onClose={() => setCreating(false)} /> : null}
      {executing ? <TaskExecuteDialog task={executing} onClose={() => setExecuting(null)} /> : null}
    </section>
  );
}
