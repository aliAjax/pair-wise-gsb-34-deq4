import { create } from "zustand";
import {
  getCurrentChecklist,
  listChecklistVersion,
  publishChecklist
} from "../api/ChecklistVersion";
import type { ChecklistVersion } from "../types/ChecklistVersion";

type State = {
  rows: ChecklistVersion[];
  loading: boolean;
  publishing: boolean;
  load: (taskType?: string) => Promise<void>;
  loadCurrent: (taskType: string) => Promise<ChecklistVersion | null>;
  publish: (versionId: number) => Promise<ChecklistVersion>;
};

export const useChecklistVersionStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  publishing: false,
  async load(taskType) {
    set({ loading: true });
    set({ rows: await listChecklistVersion(taskType), loading: false });
  },
  async loadCurrent(taskType) {
    return getCurrentChecklist(taskType);
  },
  async publish(versionId) {
    set({ publishing: true });
    try {
      const version = await publishChecklist(versionId);
      await get().load();
      return version;
    } finally {
      set({ publishing: false });
    }
  }
}));
