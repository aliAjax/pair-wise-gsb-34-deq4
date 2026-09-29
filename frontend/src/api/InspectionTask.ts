import type { InspectionTask } from "../types/InspectionTask";
import type { TaskSubmitPayload } from "../types/ChecklistVersion";
import type { TaskSubmitResponse } from "../types/TaskSubmitResponse";

const endpoint = "/api/inspection-task";

export interface CreateTaskInput {
  building_id: number;
  inspector_id: number;
  plan_date: string;
  task_type: string;
  created_by?: number;
}

export async function listInspectionTask(): Promise<InspectionTask[]> {
  const res = await fetch(endpoint);
  if (!res.ok) throw new Error(`list inspection task failed: ${res.status}`);
  return await res.json();
}

export async function createInspectionTask(input: CreateTaskInput): Promise<InspectionTask> {
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });
  if (!res.ok) throw await res.json().catch(() => ({ message: String(res.status) }));
  return await res.json();
}

export async function submitInspectionTask(
  taskId: number,
  payload: TaskSubmitPayload
): Promise<TaskSubmitResponse> {
  const res = await fetch(`${endpoint}/${taskId}/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw await res.json().catch(() => ({ message: String(res.status) }));
  return await res.json();
}
