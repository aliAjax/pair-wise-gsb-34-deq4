import { useCallback, useState } from "react";
import { submitInspectionTask } from "../api/InspectionTask";
import { ERROR_MESSAGES } from "../constants/errorMessages";
import type { ChecklistItemInput } from "../types/ChecklistVersion";
import type { TaskSubmitResponse } from "../types/TaskSubmitResponse";

interface UseHazardFlowResult {
  submitting: boolean;
  error: string;
  lastResponse: TaskSubmitResponse | null;
  submit: (taskId: number, results: ChecklistItemInput[]) => Promise<TaskSubmitResponse | null>;
}

/**
 * 提交巡检并串联隐患流程：后端按任务固定版本判级，
 * 异常项生成隐患单，同设备未关闭隐患合并并累计发现次数。
 */
export function useHazardFlow(): UseHazardFlowResult {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [lastResponse, setLastResponse] = useState<TaskSubmitResponse | null>(null);

  const submit = useCallback(async (taskId: number, results: ChecklistItemInput[]) => {
    setSubmitting(true);
    setError("");
    try {
      const response = await submitInspectionTask(taskId, { results, actor_id: 1 });
      setLastResponse(response);
      return response;
    } catch (err) {
      const code = (err as { code?: string })?.code;
      setError(code && code in ERROR_MESSAGES
        ? ERROR_MESSAGES[code as keyof typeof ERROR_MESSAGES]
        : "提交失败，请稍后重试");
      return null;
    } finally {
      setSubmitting(false);
    }
  }, []);

  return { submitting, error, lastResponse, submit };
}
