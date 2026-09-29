import { create } from "zustand";
import { closeHazardTicket, listHazardTicket } from "../api/HazardTicket";
import type { HazardTicket } from "../types/HazardTicket";

type State = {
  rows: HazardTicket[];
  loading: boolean;
  load: () => Promise<void>;
  close: (ticketId: number, note?: string) => Promise<void>;
};

export const useHazardTicketStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  async load() {
    set({ loading: true });
    try {
      set({ rows: await listHazardTicket(), loading: false });
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },
  async close(ticketId, note = "") {
    await closeHazardTicket(ticketId, 1, note);
    set({ rows: get().rows.map((row) => (row.id === ticketId
      ? { ...row, rectify_status: "CLOSED", closed_at: new Date().toISOString() }
      : row)) });
  }
}));
