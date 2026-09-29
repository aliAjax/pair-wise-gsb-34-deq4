import type { ResultStatus } from "../constants/ResultStatus";

export interface InspectionResult {
  id: number;
  task_id: number;
  device_id: number;
  item_code: string;
  result_status: ResultStatus | string;
  // 按任务固定版本判出的等级
  judged_severity?: string;
  checklist_version?: string;
  measured_value: string;
  photo_url: string;
  note: string;
  submitted_at?: string;
}
