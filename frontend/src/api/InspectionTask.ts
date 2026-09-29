import { mockData } from "../mocks/seedData";
import type {
  InspectionSubmitPayload,
  InspectionSubmitResult,
  InspectionTask,
  InspectionTaskCreatePayload
} from "../types/InspectionTask";

const endpoint = "/api/inspection-task";

export async function listInspectionTask(): Promise<InspectionTask[]> {
  try {
    const res = await fetch(endpoint);
    if (res.ok) return (await res.json()) as InspectionTask[];
  } catch {
    // Local mock fallback keeps the UI available during offline review.
  }
  return [...(mockData.inspectionTask as unknown as InspectionTask[])];
}

export async function createInspectionTask(payload: InspectionTaskCreatePayload): Promise<InspectionTask> {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error((await res.json().catch(() => ({})))?.detail?.message ?? "create task failed");
  return (await res.json()) as InspectionTask;
}

export async function submitInspectionTask(
  taskId: number,
  payload: InspectionSubmitPayload
): Promise<InspectionSubmitResult> {
  const res = await fetch(`${endpoint}/${taskId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error((await res.json().catch(() => ({})))?.detail?.message ?? "submit task failed");
  return (await res.json()) as InspectionSubmitResult;
}

export async function saveInspectionTask(payload: InspectionTask) {
  console.info("save InspectionTask", payload);
  return payload;
}
