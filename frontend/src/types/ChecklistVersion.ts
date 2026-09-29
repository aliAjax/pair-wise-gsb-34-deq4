export interface ChecklistRule {
  kind: "options" | "threshold" | "presence";
  normal?: string[];
  min?: number;
  max?: number;
  unit?: string;
  must?: boolean;
}

export interface ChecklistItem {
  item_code: string;
  item_name: string;
  device_type?: string | null;
  rule: ChecklistRule;
  fail_severity?: string | null;
}

export interface ChecklistVersion {
  id: number;
  task_type: string;
  version: string;
  status: "DRAFT" | "PUBLISHED" | "ARCHIVED";
  remark: string;
  created_by: number;
  published_by: number | null;
  created_at: string;
  published_at: string | null;
  archived_at?: string | null;
  items: ChecklistItem[];
}

export interface ChecklistItemInput {
  item_code: string;
  measured_value: string;
  result_status?: string;
  photo_url?: string;
  note?: string;
  device_id?: number | null;
}

export interface TaskSubmitPayload {
  results: ChecklistItemInput[];
  actor_id?: number;
}
