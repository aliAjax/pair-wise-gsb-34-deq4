"""清单判级器：提交时严格按任务固定版本（pinned_items）的规则判定。

绝不读取当前最新发布版本，保证"提交按建任务时的版本判定"。
"""
from src.constants.result_status import ResultStatus


class ChecklistGrader:
    @staticmethod
    def grade(item: dict, measured_value: str) -> dict:
        rule_type = item.get("rule_type")
        severity = item.get("severity", "MEDIUM")
        if rule_type == "NUMERIC":
            return ChecklistGrader._grade_numeric(item, measured_value, severity)
        if rule_type == "CHOICE":
            allowed = item.get("allowed_values") or []
            normalized = (measured_value or "").strip()
            if normalized and normalized in allowed:
                return ChecklistGrader._normal()
            return ChecklistGrader._abnormal(severity)
        if rule_type == "TEXT":
            abnormal_value = item.get("abnormal_value") or "ABNORMAL"
            if (measured_value or "").strip() == abnormal_value:
                return ChecklistGrader._abnormal(severity)
            return ChecklistGrader._normal()
        # 未知规则按缺测处理为待处理，避免误判
        return {"result_status": ResultStatus[0], "judged_severity": ""}

    @staticmethod
    def _grade_numeric(item: dict, measured_value: str, severity: str) -> dict:
        try:
            value = float(measured_value)
        except (TypeError, ValueError):
            return {"result_status": ResultStatus[0], "judged_severity": ""}
        c_min, c_max = item.get("critical_min"), item.get("critical_max")
        if c_min is not None and value < float(c_min):
            return ChecklistGrader._abnormal("CRITICAL")
        if c_max is not None and value > float(c_max):
            return ChecklistGrader._abnormal("CRITICAL")
        min_value, max_value = item.get("min_value"), item.get("max_value")
        if min_value is not None and value < float(min_value):
            return ChecklistGrader._abnormal(severity)
        if max_value is not None and value > float(max_value):
            return ChecklistGrader._abnormal(severity)
        return ChecklistGrader._normal()

    @staticmethod
    def _normal() -> dict:
        return {"result_status": ResultStatus[1], "judged_severity": "NORMAL"}

    @staticmethod
    def _abnormal(severity: str) -> dict:
        return {"result_status": ResultStatus[2], "judged_severity": severity}
