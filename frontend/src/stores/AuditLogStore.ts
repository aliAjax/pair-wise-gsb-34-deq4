import { create } from "zustand";
import { listAuditLog } from "../api/AuditLog";
import type { AuditLog } from "../types/AuditLog";

type State = {
  rows: AuditLog[];
  loading: boolean;
  load: (params?: { target_type?: string; target_id?: string | number }) => Promise<void>;
};

export const useAuditLogStore = create<State>((set) => ({
  rows: [],
  loading: false,
  async load(params) {
    set({ loading: true });
    set({ rows: await listAuditLog(params), loading: false });
  }
}));
