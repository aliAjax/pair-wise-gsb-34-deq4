import type { ChecklistItem } from "./ChecklistVersion";

export interface InspectionTask {
  id: number;
  building_id: number;
  inspector_id: number;
  plan_date: string;
  task_type: string;
  status: string;
  checklist_version: string;
  checklist_version_id: number;
  version_pinned_at: string;
  created_by: number;
  version_notice: string;
  finished_at: string;
  // 建任务时冻结的检查项快照，执行期间不随后续发布变化
  checklist_snapshot: ChecklistItem[];
}
