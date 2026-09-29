export interface InspectionResult {
  id: number;
  task_id: number;
  device_id: number | null;
  item_code: string;
  result_status: string;
  measured_value: string;
  photo_url: string;
  note: string;
  // 按任务固定版本判级的结论
  outcome: "NORMAL" | "ABNORMAL" | "NOT_CHECKED" | "";
  checklist_version: string;
  graded_at: string;
}
