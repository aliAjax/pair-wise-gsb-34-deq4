import { mockData } from "../mocks/seedData";
import type { HazardTicket } from "../types/HazardTicket";

const endpoint = "/api/hazard-ticket";

export async function listHazardTicket(): Promise<HazardTicket[]> {
  try {
    const res = await fetch(endpoint);
    if (res.ok) return await res.json();
  } catch {
    // Local mock fallback keeps the UI available during offline review.
  }
  return [...(mockData.hazardTicket as unknown as HazardTicket[])];
}

export async function closeHazardTicket(ticketId: number, rectifyNote = ""): Promise<HazardTicket> {
  const res = await fetch(`${endpoint}/${ticketId}/close`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rectify_note: rectifyNote })
  });
  if (!res.ok) throw new Error("close hazard ticket failed");
  return await res.json();
}

export async function saveHazardTicket(payload: HazardTicket) {
  console.info("save HazardTicket", payload);
  return payload;
}
