import { formatRisk } from "../../utils/formatters";

export interface HazardSeverityTagProps {
  value?: string;
}

export function HazardSeverityTag({ value = "MEDIUM" }: HazardSeverityTagProps) {
  const cls = `sev sev-${String(value).toLowerCase()}`;
  return <span className={cls}>{formatRisk(value)}</span>;
}
