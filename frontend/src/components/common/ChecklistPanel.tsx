import { ChecklistPublishStatusText, ChecklistRuleTypeText } from "../../constants/ChecklistVersion";
import { formatRisk } from "../../utils/formatters";
import type { ChecklistItem, ChecklistVersion } from "../../types/ChecklistVersion";
import { StatusBadge } from "./StatusBadge";

export interface ChecklistPanelProps {
  // 面板展示的始终是任务固定版本（pinned snapshot）或某个已发布版本，不随后续发布变化
  version?: Pick<ChecklistVersion, "version" | "status" | "remark"> | null;
  items?: ChecklistItem[];
  // 每项当前录入值与判级结果
  values?: Record<string, { measured_value?: string; result_status?: string; judged_severity?: string }>;
  editable?: boolean;
  onChange?: (itemCode: string, measuredValue: string) => void;
}

const ruleHint = (item: ChecklistItem): string => {
  if (item.rule_type === "NUMERIC") {
    return `正常 ${item.min_value ?? "-∞"} ~ ${item.max_value ?? "+∞"}，临界 ${item.critical_min ?? "-∞"} / ${item.critical_max ?? "+∞"}`;
  }
  if (item.rule_type === "CHOICE") {
    return `正常值：${(item.allowed_values ?? []).join(" / ")}`;
  }
  return `异常值：${item.abnormal_value ?? "ABNORMAL"}`;
};

export function ChecklistPanel({ version, items = [], values = {}, editable = false, onChange }: ChecklistPanelProps) {
  return (
    <div className="panel checklist-panel">
      <div className="panel-head">
        <h2>
          检查项清单 {version ? `v${version.version}` : ""}
          {version ? <StatusBadge value={ChecklistPublishStatusText[version.status] ?? version.status} /> : null}
        </h2>
        {version?.remark ? <span className="muted">{version.remark}</span> : null}
      </div>
      <div className="checklist-items">
        {items.length === 0 ? <p className="muted">该任务未固定清单版本</p> : null}
        {items.map((item) => {
          const value = values[item.item_code];
          return (
            <label key={item.item_code} className="checklist-item">
              <div>
                <strong>
                  {item.item_name} <code>{item.item_code}</code>
                </strong>
                <span className="muted">
                  {ChecklistRuleTypeText[item.rule_type]} · 默认等级 {formatRisk(item.severity)} · {ruleHint(item)}
                </span>
              </div>
              <div className="checklist-input">
                {item.rule_type === "CHOICE" ? (
                  <select
                    value={value?.measured_value ?? ""}
                    disabled={!editable}
                    onChange={(event) => onChange?.(item.item_code, event.target.value)}
                  >
                    <option value="" disabled>
                      请选择
                    </option>
                    {(item.allowed_values ?? []).map((choice) => (
                      <option key={choice} value={choice}>
                        {choice}
                      </option>
                    ))}
                    <option value="ABNORMAL">ABNORMAL</option>
                  </select>
                ) : (
                  <input
                    value={value?.measured_value ?? ""}
                    disabled={!editable}
                    placeholder="录入测量值"
                    onChange={(event) => onChange?.(item.item_code, event.target.value)}
                  />
                )}
                {value?.result_status ? <StatusBadge value={value.result_status} /> : null}
                {value?.judged_severity && value.judged_severity !== "NORMAL" ? (
                  <span className={`sev sev-${value.judged_severity.toLowerCase()}`}>{formatRisk(value.judged_severity)}</span>
                ) : null}
              </div>
            </label>
          );
        })}
      </div>
    </div>
  );
}
