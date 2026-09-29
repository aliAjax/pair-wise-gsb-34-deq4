import type { ChecklistItem, ChecklistVersion } from "../types/ChecklistVersion";

export const createDefaultChecklistItem = (overrides: Partial<ChecklistItem> = {}): ChecklistItem => ({
  item_code: "ITEM_CODE",
  item_name: "新建检查项",
  rule_type: "TEXT",
  device_type: "HYDRANT",
  severity: "MEDIUM",
  min_value: null,
  max_value: null,
  critical_min: null,
  critical_max: null,
  allowed_values: [],
  abnormal_value: "ABNORMAL",
  required: true,
  ...overrides
});

export const createDefaultChecklistVersion = (overrides: Partial<ChecklistVersion> = {}): ChecklistVersion => ({
  id: 0,
  task_type: "HYDRANT",
  scope_key: "DEFAULT",
  version: 1,
  status: "DRAFT",
  items: [],
  published_at: "",
  published_by: null,
  created_at: "",
  created_by: null,
  remark: "",
  ...overrides
});

export const createChecklistVersionForm = createDefaultChecklistVersion;
export const createChecklistVersionResponse = createDefaultChecklistVersion;
