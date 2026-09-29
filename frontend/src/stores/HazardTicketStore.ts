import { create } from "zustand";
import { closeHazardTicket, listHazardTicket } from "../api/HazardTicket";
import type { HazardTicket } from "../types/HazardTicket";

type State = {
  rows: HazardTicket[];
  loading: boolean;
  load: () => Promise<void>;
  close: (ticketId: number, rectifyNote?: string) => Promise<HazardTicket>;
};

export const useHazardTicketStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  async load() {
    set({ loading: true });
    set({ rows: await listHazardTicket(), loading: false });
  },
  async close(ticketId, rectifyNote = "") {
    const ticket = await closeHazardTicket(ticketId, rectifyNote);
    await get().load();
    return ticket;
  }
}));
