export interface TimelineEntry {
  id: string | number;
  title: string;
  description?: string;
  at?: string;
  tone?: string;
}

/** 通用时间线：用于展示发布/提交/合并等可追溯事件。 */
export function TimelineList({ entries = [] }: { entries?: TimelineEntry[] }) {
  if (entries.length === 0) {
    return <p className="muted">暂无追溯记录</p>;
  }
  return (
    <ol className="timeline">
      {entries.map((entry) => (
        <li key={entry.id} className={`timeline-entry ${entry.tone ?? ""}`}>
          <div className="timeline-dot" />
          <div className="timeline-body">
            <div className="timeline-title">{entry.title}</div>
            {entry.description ? <div className="timeline-desc">{entry.description}</div> : null}
            {entry.at ? <time className="timeline-at">{entry.at}</time> : null}
          </div>
        </li>
      ))}
    </ol>
  );
}
