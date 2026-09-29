import type { ChecklistItem } from "../../types/ChecklistVersion";

interface ChecklistPanelProps {
  version: string;
  items: ChecklistItem[];
  values?: Record<string, string>;
  onValueChange?: (itemCode: string, value: string) => void;
  readonly?: boolean;
}

const ruleHint: Record<string, string> = {
  options: "选择项判定",
  threshold: "阈值区间判定",
  presence: "有无判定"
};

/**
 * 巡检清单面板：渲染任务固定版本快照中的检查项。
 * 数据来自建任务时冻结的快照，清单后续发布不会改变此处内容。
 */
export function ChecklistPanel({ version, items, values = {}, onValueChange, readonly }: ChecklistPanelProps) {
  return (
    <div className="checklist-panel">
      <div className="checklist-panel-head">
        <strong>固定版本 v{version}</strong>
        <span className="muted">{items.length} 个检查项</span>
      </div>
      <ul className="checklist-items">
        {items.map((item) => (
          <li key={item.item_code} className="checklist-item">
            <div className="checklist-item-main">
              <span className="checklist-item-code">{item.item_code}</span>
              <span className="checklist-item-name">{item.item_name}</span>
              <span className="checklist-item-rule">{ruleHint[item.rule.kind] ?? item.rule.kind}</span>
              {item.fail_severity ? <span className={`sev sev-${item.fail_severity.toLowerCase()}`}>异常:{item.fail_severity}</span> : null}
            </div>
            {readonly ? (
              <span className="checklist-item-value">{values[item.item_code] ?? "—"}</span>
            ) : (
              <input
                aria-label={`检查项 ${item.item_code} 测量值`}
                value={values[item.item_code] ?? ""}
                placeholder="录入测量值"
                onChange={(event) => onValueChange?.(item.item_code, event.target.value)}
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
