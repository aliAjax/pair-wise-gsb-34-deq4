import { create } from "zustand";
import {
  createInspectionTask,
  listInspectionTask,
  submitInspectionTask,
  type CreateTaskInput
} from "../api/InspectionTask";
import type { InspectionTask } from "../types/InspectionTask";
import type { TaskSubmitPayload } from "../types/ChecklistVersion";
import type { TaskSubmitResponse } from "../types/TaskSubmitResponse";

type State = {
  rows: InspectionTask[];
  loading: boolean;
  lastNotice: string;
  lastSubmit: TaskSubmitResponse | null;
  load: () => Promise<void>;
  create: (input: CreateTaskInput) => Promise<InspectionTask>;
  submit: (taskId: number, payload: TaskSubmitPayload) => Promise<TaskSubmitResponse>;
};

export const useInspectionTaskStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  lastNotice: "",
  lastSubmit: null,
  async load() {
    set({ loading: true });
    try {
      set({ rows: await listInspectionTask(), loading: false });
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },
  async create(input) {
    // 建任务时后端固定当时已发布版本；发布与建任务同时发生时通过 version_notice 提示创建人
    const created = await createInspectionTask(input);
    set({ rows: [...get().rows, created], lastNotice: created.version_notice || "" });
    return created;
  },
  async submit(taskId, payload) {
    const result = await submitInspectionTask(taskId, payload);
    set({
      lastSubmit: result,
      rows: get().rows.map((row) => (row.id === taskId ? result.task : row))
    });
    return result;
  }
}));
