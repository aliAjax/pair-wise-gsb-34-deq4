import type { HazardTicket } from "../types/HazardTicket";

export const createDefaultHazardTicket = (overrides: Partial<HazardTicket> = {}): HazardTicket => ({
  id: 0,
  result_id: 0,
  first_result_id: 0,
  latest_result_id: 0,
  device_id: null,
  severity: "MEDIUM",
  owner_id: 1,
  deadline: "",
  rectify_status: "OPEN",
  rectify_note: "",
  closed_at: "",
  found_count: 1,
  created_at: "",
  updated_at: "",
  ...overrides
});

export const createHazardTicketForm = createDefaultHazardTicket;
export const createHazardTicketResponse = createDefaultHazardTicket;
