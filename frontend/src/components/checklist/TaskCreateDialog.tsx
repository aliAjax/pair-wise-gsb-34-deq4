import { useEffect, useMemo, useState } from "react";
import { DeviceType, DeviceTypeText } from "../../constants/DeviceType";
import { listBuilding } from "../../api/Building";
import { getCurrentChecklist } from "../../api/ChecklistVersion";
import { useInspectionTaskStore } from "../../stores/InspectionTaskStore";
import type { Building } from "../../types/Building";
import type { ChecklistVersion } from "../../types/ChecklistVersion";

export function TaskCreateDialog({ onClose }: { onClose: () => void }) {
  const create = useInspectionTaskStore((state) => state.create);
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [taskType, setTaskType] = useState<string>(DeviceType[1]);
  const [buildingId, setBuildingId] = useState<number>(1);
  const [current, setCurrent] = useState<ChecklistVersion | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void listBuilding().then((rows) => {
      setBuildings(rows);
      if (rows[0]) setBuildingId(rows[0].id);
    });
  }, []);

  // 打开表单时记录当时已发布版本；提交时由后端检测发布并发
  useEffect(() => {
    void getCurrentChecklist(taskType).then(setCurrent);
  }, [taskType]);

  const itemCount = current?.items.length ?? 0;
  const canSubmit = useMemo(() => current?.status === "PUBLISHED" && itemCount > 0, [current, itemCount]);

  const submit = async () => {
    if (!current || !canSubmit) return;
    setSubmitting(true);
    setError("");
    try {
      await create({
        building_id: buildingId,
        task_type: taskType,
        expected_version_id: current.id
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "创建失败");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-mask" onClick={onClose}>
      <div className="modal" onClick={(event) => event.stopPropagation()}>
        <h2>创建巡检任务</h2>
        <p className="muted">任务创建后固定当前已发布清单版本，执行期间不再随清单发布变化。</p>
        <label className="form-row">
          <span>设备类型</span>
          <select value={taskType} onChange={(event) => setTaskType(event.target.value)}>
            {DeviceType.map((value) => (
              <option key={value} value={value}>
                {DeviceTypeText[value]}
              </option>
            ))}
          </select>
        </label>
        <label className="form-row">
          <span>楼栋</span>
          <select value={buildingId} onChange={(event) => setBuildingId(Number(event.target.value))}>
            {buildings.map((building) => (
              <option key={building.id} value={building.id}>
                {building.name}
              </option>
            ))}
          </select>
        </label>
        <div className="form-row version-preview">
          <span>当前已发布版本</span>
          {current ? (
            <strong>
              v{current.version} · {itemCount} 个检查项
            </strong>
          ) : (
            <strong className="warn">该类型暂无已发布清单</strong>
          )}
        </div>
        {error ? <p className="error">{error}</p> : null}
        <div className="modal-actions">
          <button type="button" onClick={onClose}>
            取消
          </button>
          <button type="button" className="primary" disabled={submitting || !canSubmit} onClick={submit}>
            {submitting ? "创建中…" : "固定该版本并创建"}
          </button>
        </div>
      </div>
    </div>
  );
}
