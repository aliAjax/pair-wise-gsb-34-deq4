import type { ChecklistItem } from "./ChecklistVersion";

export interface InspectionTask {
  id: number;
  building_id: number;
  inspector_id: number;
  plan_date: string;
  task_type: string;
  status: string;
  checklist_version: string;
  finished_at: string;
  // 建任务时固定的清单版本主键/版本号与检查项快照
  checklist_version_id?: number;
  version_no?: number;
  pinned_items?: ChecklistItem[];
  created_at?: string;
  created_by?: number;
  // 发布与建任务并发时给创建人的提示
  version_notice?: string;
  results?: InspectionResultLike[];
}

export interface InspectionResultLike {
  id: number;
  item_code: string;
  result_status: string;
  judged_severity?: string;
  measured_value: string;
}

export interface InspectionTaskCreatePayload {
  building_id: number;
  inspector_id?: number;
  plan_date?: string;
  task_type: string;
  // 打开创建表单时看到的已发布版本，提交时用于检测发布并发
  expected_version_id?: number;
}

export interface InspectionEntry {
  device_id: number;
  item_code: string;
  measured_value: string;
  photo_url?: string;
  note?: string;
}

export interface InspectionSubmitPayload {
  entries: InspectionEntry[];
}

export interface InspectionSubmitResult {
  task: InspectionTask;
  results: InspectionResultLike[];
  abnormal_count: number;
  created_tickets: unknown[];
  merged_tickets: unknown[];
}
