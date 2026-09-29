import type { AuditLog } from "../types/AuditLog";

const endpoint = "/api/audit-log";

export async function listAuditLog(params?: { target_type?: string; target_id?: string | number }): Promise<AuditLog[]> {
  const query = new URLSearchParams();
  if (params?.target_type) query.set("target_type", params.target_type);
  if (params?.target_id !== undefined) query.set("target_id", String(params.target_id));
  const suffix = query.toString() ? `?${query.toString()}` : "";
  const res = await fetch(`${endpoint}${suffix}`);
  if (!res.ok) return [];
  return (await res.json()) as AuditLog[];
}
