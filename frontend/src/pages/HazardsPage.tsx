import { useEffect, useState } from "react";
import { HazardSeverityTag } from "../components/common/HazardSeverityTag";
import { StatusBadge } from "../components/common/StatusBadge";
import { TimelineList } from "../components/common/TimelineList";
import { listAuditLog } from "../api/AuditLog";
import { RectifyStatusText } from "../constants/RectifyStatus";
import { useHazardFlow } from "../hooks/useHazardFlow";
import { useHazardTicketStore } from "../stores/HazardTicketStore";
import { formatDate } from "../utils/formatters";
import type { AuditLog } from "../types/AuditLog";

export function HazardsPage() {
  const { rows, loading, load, close } = useHazardTicketStore();
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [busyId, setBusyId] = useState<number | null>(null);

  // 仅展示合并/关闭相关追溯
  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    void listAuditLog({ target_type: "HazardTicket" }).then((items) => setLogs(items.slice(-15).reverse()));
  }, [rows.length]);

  // 共享 hook：隐患流分页
  const { pageRows, page, setPage, pageSize, total } = useHazardFlow(rows);

  const closeTicket = async (ticketId: number) => {
    setBusyId(ticketId);
    try {
      await close(ticketId, "复验合格，关闭隐患单");
      const items = await listAuditLog({ target_type: "HazardTicket" });
      setLogs(items.slice(-15).reverse());
    } finally {
      setBusyId(null);
    }
  };

  const openCount = rows.filter((ticket) => ticket.rectify_status !== "CLOSED").length;

  return (
    <section className="page">
      <header className="page-head">
        <div>
          <p className="eyebrow">fire-inspect</p>
          <h1>隐患整改</h1>
          <p className="muted">同一设备存在未关闭隐患时，新异常会合并到原单并累计发现次数，关闭后才会重新开单。</p>
        </div>
        <StatusBadge value={`未关闭 ${openCount}`} />
      </header>

      <div className="workbench hazards-layout">
        <div className="panel wide">
          <h2>隐患单（合并去重）</h2>
          {loading ? <p className="muted">加载中…</p> : null}
          <div className="table hazard-table">
            <div className="row hazard-head">
              <span>隐患单</span>
              <span>设备</span>
              <span>等级</span>
              <span>发现次数</span>
              <span>状态</span>
              <span>最近发现</span>
              <span>操作</span>
            </div>
            {pageRows.map((ticket) => (
              <article key={ticket.id} className="row hazard-row">
                <span>
                  <strong>#{ticket.id}</strong>
                  <em className="muted"> 结果 {ticket.result_id}</em>
                </span>
                <span>设备 {ticket.device_id ?? "-"}</span>
                <HazardSeverityTag value={ticket.severity} />
                <span className="found-count">×{ticket.found_count ?? 1}</span>
                <StatusBadge value={RectifyStatusText[ticket.rectify_status as keyof typeof RectifyStatusText] ?? ticket.rectify_status} />
                <span className="muted">{ticket.last_found_at ? formatDate(ticket.last_found_at) : "-"}</span>
                <button
                  type="button"
                  disabled={ticket.rectify_status === "CLOSED" || busyId === ticket.id}
                  onClick={() => void closeTicket(ticket.id)}
                >
                  {ticket.rectify_status === "CLOSED" ? "已关闭" : "复验关闭"}
                </button>
              </article>
            ))}
          </div>
          <p className="muted pagination">
            第 {page} / {Math.max(1, Math.ceil(total / pageSize))} 页 · 共 {total} 张
            <button type="button" disabled={page <= 1} onClick={() => setPage(page - 1)}>
              上一页
            </button>
            <button type="button" disabled={page * pageSize >= total} onClick={() => setPage(page + 1)}>
              下一页
            </button>
          </p>
        </div>
        <TimelineList
          title="隐患合并与关闭追溯"
          entries={logs.map((log) => ({
            id: log.id,
            action: log.action,
            actor: log.actor,
            detail: log.detail,
            created_at: log.created_at
          }))}
        />
      </div>
    </section>
  );
}
