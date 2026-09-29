import type { ChecklistRuleType, ChecklistPublishStatus } from "../constants/ChecklistVersion";
import type { HazardSeverity } from "../constants/HazardSeverity";

export interface ChecklistItem {
  item_code: string;
  item_name: string;
  rule_type: ChecklistRuleType;
  device_type: string;
  severity: HazardSeverity;
  min_value?: number | null;
  max_value?: number | null;
  critical_min?: number | null;
  critical_max?: number | null;
  allowed_values?: string[];
  abnormal_value?: string | null;
  required?: boolean;
}

export interface ChecklistVersion {
  id: number;
  task_type: string;
  scope_key: string;
  version: number;
  status: ChecklistPublishStatus;
  items: ChecklistItem[];
  published_at: string;
  published_by?: number | null;
  created_at: string;
  created_by?: number | null;
  remark: string;
}

export interface ChecklistVersionCreatePayload {
  task_type: string;
  remark?: string;
  items: ChecklistItem[];
}
