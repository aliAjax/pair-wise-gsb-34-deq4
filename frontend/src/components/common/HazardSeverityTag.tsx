const severityText: Record<string, string> = {
  LOW: "低危",
  MEDIUM: "中危",
  HIGH: "高危",
  CRITICAL: "紧急"
};

export function HazardSeverityTag({ value }: { value: string }) {
  return (
    <span className={`sev sev-${String(value).toLowerCase()}`} title="隐患等级">
      {severityText[value] ?? value}
    </span>
  );
}
