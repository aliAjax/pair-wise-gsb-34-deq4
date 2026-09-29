import type { HazardTicket } from "./HazardTicket";
import type { InspectionResult } from "./InspectionResult";
import type { InspectionTask } from "./InspectionTask";

export interface TaskSubmitResponse {
  task: InspectionTask;
  results: InspectionResult[];
  hazard_tickets: HazardTicket[];
  merged_hazard_ids: number[];
}
