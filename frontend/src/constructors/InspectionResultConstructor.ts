import type { InspectionResult } from "../types/InspectionResult";

export const createDefaultInspectionResult = (overrides: Partial<InspectionResult> = {}): InspectionResult => ({
  id: 0,
  task_id: 0,
  device_id: null,
  item_code: "",
  result_status: "DONE",
  measured_value: "",
  photo_url: "",
  note: "",
  outcome: "",
  checklist_version: "",
  graded_at: "",
  ...overrides
});

export const createInspectionResultForm = createDefaultInspectionResult;
export const createInspectionResultResponse = createDefaultInspectionResult;
