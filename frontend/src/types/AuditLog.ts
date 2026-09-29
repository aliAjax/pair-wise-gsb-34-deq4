export interface AuditLog {
  id: number;
  actor_id: number | string;
  action: string;
  target_type: string;
  target_id: string;
  detail: Record<string, unknown>;
  created_at: string;
}
