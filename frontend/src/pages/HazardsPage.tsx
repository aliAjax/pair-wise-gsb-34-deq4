import { useEffect, useMemo, useState } from "react";
import { HazardSeverityTag } from "../components/common/HazardSeverityTag";
import { StatusBadge } from "../components/common/StatusBadge";
import { TimelineList, type TimelineEntry } from "../components/common/TimelineList";
import { useHazardTicketStore } from "../stores/HazardTicketStore";
import { listAuditLog } from "../api/AuditLog";
import type { AuditLog } from "../types/AuditLog";
import { HAZARD_OPEN_STATUSES } from "../constants/HazardRectifyStatus";
import { formatDate } from "../utils/formatters";

export function HazardsPage() {
  const store = useHazardTicketStore();
  const [logs, setLogs] = useState<AuditLog[]>([]);

  useEffect(() => {
    store.load();
    listAuditLog({ targetType: "HazardTicket" }).then(setLogs).catch(() => setLogs([]));
  }, []);

  const openCount = useMemo(
    () => store.rows.filter((ticket) => HAZARD_OPEN_STATUSES.includes(ticket.rectify_status)).length,
    [store.rows]
  );

  const timeline: TimelineEntry[] = useMemo(() => logs.slice(0, 15).map((log) => ({
    id: log.id,
    title: log.action === "HazardTicket.merge"
      ? `隐患 #${log.target_id} 合并（累计发现 ${String((log.detail as { found_count?: number }).found_count ?? "")} 次）`
      : `${log.action} #${log.target_id}`,
    description: log.detail ? JSON.stringify(log.detail) : "",
    at: formatDate(log.created_at),
    tone: log.action === "HazardTicket.merge" ? "abnormal" : ""
  })), [logs]);

  const handleClose = async (ticketId: number) => {
    await store.close(ticketId, "复验合格，关闭隐患");
    listAuditLog({ targetType: "HazardTicket" }).then(setLogs);
  };

  return (
    <section className="page-stack">
      <div className="panel">
        <h2>隐患整改单</h2>
        <p className="muted">未关闭 {openCount} 单。同一设备再次发现异常时合并到原单并累计发现次数，关闭后再发现将新建单据。</p>
        <div className="table">
          {store.rows.map((ticket) => (
            <article key={ticket.id} className="row hazard-row">
              <strong>隐患 #{ticket.id}</strong>
              <HazardSeverityTag value={ticket.severity} />
              <StatusBadge value={ticket.rectify_status} />
              <span>设备 {ticket.device_id ?? "—"}</span>
              <span className={ticket.found_count > 1 ? "found-count" : ""}>发现 {ticket.found_count} 次</span>
              <span className="muted">最近结果 #{ticket.latest_result_id}</span>
              {HAZARD_OPEN_STATUSES.includes(ticket.rectify_status) ? (
                <button type="button" onClick={() => handleClose(ticket.id)}>复验关闭</button>
              ) : (
                <span className="muted">关闭于 {formatDate(ticket.closed_at)}</span>
              )}
            </article>
          ))}
        </div>
      </div>

      <div className="panel">
        <h2>合并与关闭追溯</h2>
        <TimelineList entries={timeline} />
      </div>
    </section>
  );
}
