import type { ChecklistVersion } from "../types/ChecklistVersion";

const endpoint = "/api/checklist-version";

export async function listChecklistVersion(): Promise<ChecklistVersion[]> {
  const res = await fetch(endpoint);
  if (!res.ok) throw new Error(`list checklist failed: ${res.status}`);
  return await res.json();
}

export async function publishChecklistVersion(versionId: number, actorId = 1): Promise<ChecklistVersion> {
  const res = await fetch(`${endpoint}/${versionId}/publish?actor_id=${actorId}`, { method: "POST" });
  if (!res.ok) throw await res.json().catch(() => ({ message: String(res.status) }));
  return await res.json();
}
