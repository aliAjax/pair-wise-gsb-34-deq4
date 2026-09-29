import type { HazardTicket } from "../types/HazardTicket";

const endpoint = "/api/hazard-ticket";

export async function listHazardTicket(): Promise<HazardTicket[]> {
  const res = await fetch(endpoint);
  if (!res.ok) throw new Error(`list hazard ticket failed: ${res.status}`);
  return await res.json();
}

export async function closeHazardTicket(ticketId: number, actorId = 1, note = ""): Promise<HazardTicket> {
  const params = new URLSearchParams({ actor_id: String(actorId) });
  if (note) params.set("note", note);
  const res = await fetch(`${endpoint}/${ticketId}/close?${params.toString()}`, { method: "POST" });
  if (!res.ok) throw await res.json().catch(() => ({ message: String(res.status) }));
  return await res.json();
}
