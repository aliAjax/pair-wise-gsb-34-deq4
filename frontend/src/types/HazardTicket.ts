export interface HazardTicket {
  id: number;
  result_id: number;
  first_result_id: number;
  latest_result_id: number;
  device_id: number | null;
  severity: string;
  owner_id: number;
  deadline: string;
  rectify_status: "OPEN" | "RECTIFYING" | "REVIEWING" | "CLOSED";
  rectify_note: string;
  closed_at: string;
  // 同设备未关闭隐患合并后累计的发现次数
  found_count: number;
  created_at: string;
  updated_at: string;
}
