export interface HazardTicket {
  id: number;
  result_id: number;
  severity: string;
  owner_id: number;
  deadline: string;
  rectify_status: string;
  rectify_note: string;
  closed_at: string;
  // 合并所需的设备冗余、累计发现次数与并入的异常结果
  device_id?: number;
  found_count?: number;
  merged_result_ids?: number[];
  last_found_at?: string;
  created_at?: string;
}
