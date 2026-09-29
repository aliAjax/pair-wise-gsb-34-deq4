import { mockData } from "../mocks/seedData";
import type { ChecklistVersion, ChecklistVersionCreatePayload } from "../types/ChecklistVersion";

const endpoint = "/api/checklist-version";

async function readJson<T>(res: Response): Promise<T> {
  return (await res.json()) as T;
}

export async function listChecklistVersion(task_type?: string): Promise<ChecklistVersion[]> {
  try {
    const url = task_type ? `${endpoint}?task_type=${encodeURIComponent(task_type)}` : endpoint;
    const res = await fetch(url);
    if (res.ok) return await readJson<ChecklistVersion[]>(res);
  } catch {
    // 离线评审时回退本地种子
  }
  const rows = mockData.checklistVersion as unknown as ChecklistVersion[];
  return task_type ? rows.filter((row) => row.task_type === task_type) : [...rows];
}

export async function getCurrentChecklist(task_type: string): Promise<ChecklistVersion | null> {
  try {
    const res = await fetch(`${endpoint}/current/${encodeURIComponent(task_type)}`);
    if (res.ok) return await readJson<ChecklistVersion>(res);
  } catch {
    // ignore and fallback
  }
  const rows = (mockData.checklistVersion as unknown as ChecklistVersion[])
    .filter((row) => row.task_type === task_type && row.status === "PUBLISHED")
    .sort((a, b) => b.version - a.version);
  return rows[0] ?? null;
}

export async function createChecklistDraft(payload: ChecklistVersionCreatePayload): Promise<ChecklistVersion> {
  const res = await fetch(`${endpoint}/draft`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("create checklist draft failed");
  return await readJson<ChecklistVersion>(res);
}

export async function publishChecklist(versionId: number): Promise<ChecklistVersion> {
  const res = await fetch(`${endpoint}/${versionId}/publish`, { method: "POST" });
  if (!res.ok) throw new Error("publish checklist failed");
  return await readJson<ChecklistVersion>(res);
}
