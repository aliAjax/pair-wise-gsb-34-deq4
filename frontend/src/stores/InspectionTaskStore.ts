import { create } from "zustand";
import {
  createInspectionTask,
  listInspectionTask,
  submitInspectionTask
} from "../api/InspectionTask";
import type {
  InspectionSubmitPayload,
  InspectionSubmitResult,
  InspectionTask,
  InspectionTaskCreatePayload
} from "../types/InspectionTask";

type State = {
  rows: InspectionTask[];
  loading: boolean;
  // 最近一次建任务返回的版本并发提示，由页面弹窗提示创建人
  lastVersionNotice: string;
  load: () => Promise<void>;
  create: (payload: InspectionTaskCreatePayload) => Promise<InspectionTask>;
  submit: (taskId: number, payload: InspectionSubmitPayload) => Promise<InspectionSubmitResult>;
  clearNotice: () => void;
};

export const useInspectionTaskStore = create<State>((set, get) => ({
  rows: [],
  loading: false,
  lastVersionNotice: "",
  async load() {
    set({ loading: true });
    set({ rows: await listInspectionTask(), loading: false });
  },
  async create(payload) {
    const task = await createInspectionTask(payload);
    // 发布与建任务同时发生时，后端已采用最新已发布版本，并把提示回传创建人
    set({ lastVersionNotice: task.version_notice ?? "" });
    await get().load();
    return task;
  },
  async submit(taskId, payload) {
    const result = await submitInspectionTask(taskId, payload);
    await get().load();
    return result;
  },
  clearNotice() {
    set({ lastVersionNotice: "" });
  }
}));
