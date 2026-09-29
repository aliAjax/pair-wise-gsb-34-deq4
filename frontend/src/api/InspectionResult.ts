import type { InspectionResult } from "../types/InspectionResult";

const endpoint = "/api/inspection-result";

export async function listInspectionResult(): Promise<InspectionResult[]> {
  const res = await fetch(endpoint);
  if (!res.ok) throw new Error(`list inspection result failed: ${res.status}`);
  return await res.json();
}
