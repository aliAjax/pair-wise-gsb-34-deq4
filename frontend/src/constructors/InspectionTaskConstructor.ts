import type { InspectionTask } from "../types/InspectionTask";

export const createDefaultInspectionTask = (overrides: Partial<InspectionTask> = {}): InspectionTask => ({
  id: 0,
  building_id: 1,
  inspector_id: 1,
  plan_date: "2026-09-29T09:00:00Z",
  task_type: "HYDRANT",
  status: "PLANNED",
  checklist_version: "",
  checklist_version_id: 0,
  version_pinned_at: "",
  created_by: 1,
  version_notice: "",
  finished_at: "",
  checklist_snapshot: [],
  ...overrides
});

export const createInspectionTaskForm = createDefaultInspectionTask;
export const createInspectionTaskResponse = createDefaultInspectionTask;
