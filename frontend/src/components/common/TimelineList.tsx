import { formatDate } from "../../utils/formatters";

export interface TimelineEntry {
  id: string | number;
  action: string;
  actor?: string | number;
  detail?: string;
  created_at?: string;
}

export interface TimelineListProps {
  title?: string;
  entries?: TimelineEntry[];
}

export function TimelineList({ title = "流转记录", entries = [] }: TimelineListProps) {
  return (
    <div className="panel timeline">
      <h2>{title}</h2>
      {entries.length === 0 ? <p className="muted">暂无记录</p> : null}
      <ol className="timeline-entries">
        {entries.map((entry) => (
          <li key={entry.id}>
            <div>
              <strong>{entry.action}</strong>
              {entry.actor !== undefined ? <span className="muted"> · 操作人 {entry.actor}</span> : null}
            </div>
            {entry.detail ? <p className="muted">{entry.detail}</p> : null}
            {entry.created_at ? <time className="muted">{formatDate(entry.created_at)}</time> : null}
          </li>
        ))}
      </ol>
    </div>
  );
}
