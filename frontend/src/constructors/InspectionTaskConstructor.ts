import type { ChecklistItem } from "../types/ChecklistVersion";
import type { InspectionTask, InspectionTaskCreatePayload, InspectionEntry } from "../types/InspectionTask";

export const createDefaultInspectionTask = (overrides: Partial<InspectionTask> = {}): InspectionTask => ({
  id: 1,
  building_id: 1,
  inspector_id: 1,
  plan_date: "2026-06-11T09:00:00Z",
  task_type: "HYDRANT",
  status: "PLANNED",
  checklist_version: "v1",
  checklist_version_id: 1,
  version_no: 1,
  pinned_items: [],
  finished_at: "",
  created_at: "",
  created_by: 1,
  version_notice: "",
  ...overrides
});

export const createInspectionTaskForm = (
  overrides: Partial<InspectionTaskCreatePayload> = {}
): InspectionTaskCreatePayload => ({
  building_id: 1,
  inspector_id: 1,
  plan_date: "",
  task_type: "HYDRANT",
  expected_version_id: undefined,
  ...overrides
});

export const createInspectionEntry = (
  item: ChecklistItem,
  deviceId: number,
  overrides: Partial<InspectionEntry> = {}
): InspectionEntry => ({
  device_id: deviceId,
  item_code: item.item_code,
  measured_value: "",
  photo_url: "",
  note: "",
  ...overrides
});

export const createInspectionTaskResponse = createDefaultInspectionTask;
