import { useEffect } from "react";
import { ChecklistPublishStatusText } from "../../constants/ChecklistVersion";
import { DeviceTypeText } from "../../constants/DeviceType";
import { useChecklistVersionStore } from "../../stores/ChecklistVersionStore";
import { formatDate } from "../../utils/formatters";
import { StatusBadge } from "../common/StatusBadge";
import { ChecklistPanel } from "../common/ChecklistPanel";

export interface ChecklistPublishPanelProps {
  taskType?: string;
  // 发布成功后通知任务页：新建任务应引用新版本
  onPublished?: (versionId: number) => void;
}

export function ChecklistPublishPanel({ taskType, onPublished }: ChecklistPublishPanelProps) {
  const { rows, loading, publishing, load, publish } = useChecklistVersionStore();

  useEffect(() => {
    void load(taskType);
  }, [load, taskType]);

  const versions = [...rows].sort((a, b) => b.version - a.version);

  return (
    <div className="panel">
      <div className="panel-head">
        <h2>巡检清单发布</h2>
        <span className="muted">发布后版本不可变，进行中的任务仍按建任务时的版本执行</span>
      </div>
      {loading ? <p className="muted">加载中…</p> : null}
      <div className="version-list">
        {versions.map((version) => (
          <details key={version.id} className="version-card">
            <summary>
              <strong>
                {DeviceTypeText[version.task_type as keyof typeof DeviceTypeText] ?? version.task_type} 清单 v{version.version}
              </strong>
              <StatusBadge value={ChecklistPublishStatusText[version.status]} />
              <span className="muted">{version.remark}</span>
              {version.status === "PUBLISHED" && version.published_at ? (
                <time className="muted">发布于 {formatDate(version.published_at)}</time>
              ) : (
                <span className="muted">草稿 · 未发布</span>
              )}
              {version.status === "DRAFT" ? (
                <button
                  type="button"
                  className="primary"
                  disabled={publishing}
                  onClick={(event) => {
                    event.preventDefault();
                    void publish(version.id).then(() => onPublished?.(version.id));
                  }}
                >
                  发布此版本
                </button>
              ) : null}
            </summary>
            <ChecklistPanel
              version={{ version: version.version, status: version.status, remark: version.remark }}
              items={version.items}
            />
          </details>
        ))}
      </div>
    </div>
  );
}
