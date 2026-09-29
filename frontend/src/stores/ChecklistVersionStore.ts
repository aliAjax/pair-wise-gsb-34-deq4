import { create } from "zustand";
import { listChecklistVersion, publishChecklistVersion } from "../api/ChecklistVersion";
import type { ChecklistVersion } from "../types/ChecklistVersion";

type State = {
  rows: ChecklistVersion[];
  loading: boolean;
  load: () => Promise<void>;
  publish: (versionId: number) => Promise<ChecklistVersion>;
};

export const useChecklistVersionStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  async load() {
    set({ loading: true });
    try {
      set({ rows: await listChecklistVersion(), loading: false });
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },
  async publish(versionId) {
    const published = await publishChecklistVersion(versionId);
    set({
      rows: get().rows.map((row) => {
        if (row.id === published.id) return published;
        if (row.task_type === published.task_type && row.status === "PUBLISHED") {
          return { ...row, status: "ARCHIVED" };
        }
        return row;
      })
    });
    return published;
  }
}));
