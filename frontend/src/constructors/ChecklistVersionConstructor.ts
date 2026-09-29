import type { ChecklistItem, ChecklistVersion } from "../types/ChecklistVersion";

export const createDefaultChecklistItem = (overrides: Partial<ChecklistItem> = {}): ChecklistItem => ({
  item_code: "",
  item_name: "",
  device_type: null,
  rule: { kind: "options", normal: ["NORMAL", "YES"] },
  fail_severity: "MEDIUM",
  ...overrides
});

export const createDefaultChecklistVersion = (
  overrides: Partial<ChecklistVersion> = {}
): ChecklistVersion => ({
  id: 0,
  task_type: "HYDRANT",
  version: "",
  status: "DRAFT",
  remark: "",
  created_by: 1,
  published_by: null,
  created_at: "",
  published_at: null,
  archived_at: null,
  items: [],
  ...overrides
});

export const createChecklistVersionForm = createDefaultChecklistVersion;
