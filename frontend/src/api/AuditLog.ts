import type { AuditLog } from "../types/AuditLog";

const endpoint = "/api/audit-log";

export async function listAuditLog(filter: { action?: string; targetType?: string } = {}): Promise<AuditLog[]> {
  const params = new URLSearchParams();
  if (filter.action) params.set("action", filter.action);
  if (filter.targetType) params.set("target_type", filter.targetType);
  const res = await fetch(`${endpoint}?${params.toString()}`);
  if (!res.ok) throw new Error(`list audit log failed: ${res.status}`);
  return await res.json();
}
