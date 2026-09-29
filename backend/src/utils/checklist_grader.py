"""按巡检清单版本内置规则判定结果等级。

规则与清单版本一起冻结：任务提交时只能使用任务固定版本里的规则，
后续清单再发布新版本也不会改变历史任务的判级口径。

支持的规则形式（rule 字段）：
  {"kind": "options", "normal": ["NORMAL", "YES"]}
      measured_value/result_status 命中 normal 集合为正常，否则异常
  {"kind": "threshold", "min": 0.2, "max": 0.8, "unit": "MPa"}
      数值落在闭区间内为正常，区间外为异常，无法解析数值为异常
  {"kind": "presence", "must": true}
      必须有 measured_value（且非 N/A、空串）为正常
"""
from src.constants.result_outcome import (
    RESULT_OUTCOME_NORMAL,
    RESULT_OUTCOME_ABNORMAL,
    RESULT_SEVERITY_BY_OUTCOME,
)


class GradingError(ValueError):
    """规则数据本身有问题（配置期错误），区别于提交期的未知检查项错误。"""


def _grade_options(item: dict, measured_value: str) -> str:
    normal_values = {str(v).upper() for v in (item["rule"].get("normal") or [])}
    value = (measured_value or "").strip().upper()
    return RESULT_OUTCOME_NORMAL if value in normal_values else RESULT_OUTCOME_ABNORMAL


def _grade_threshold(item: dict, measured_value: str) -> str:
    try:
        number = float(str(measured_value).strip())
    except (TypeError, ValueError):
        return RESULT_OUTCOME_ABNORMAL
    rule = item["rule"]
    lower = rule.get("min")
    upper = rule.get("max")
    if lower is not None and number < float(lower):
        return RESULT_OUTCOME_ABNORMAL
    if upper is not None and number > float(upper):
        return RESULT_OUTCOME_ABNORMAL
    return RESULT_OUTCOME_NORMAL


def _grade_presence(item: dict, measured_value: str) -> str:
    required = bool(item["rule"].get("must", True))
    present = bool((measured_value or "").strip()) and (measured_value or "").strip().upper() != "N/A"
    if required and not present:
        return RESULT_OUTCOME_ABNORMAL
    return RESULT_OUTCOME_NORMAL if present or not required else RESULT_OUTCOME_ABNORMAL


_GRADERS = {
    "options": _grade_options,
    "threshold": _grade_threshold,
    "presence": _grade_presence,
}


def grade_item(item: dict, measured_value: str) -> str:
    """按单个检查项规则判定结果，返回 normal / abnormal。"""
    rule = item.get("rule") or {}
    kind = rule.get("kind", "options")
    grader = _GRADERS.get(kind)
    if grader is None:
        raise GradingError(f"unsupported grading rule kind: {kind}")
    return grader(item, measured_value)


def severity_for_outcome(item: dict, outcome: str) -> str:
    """异常等级优先取检查项在该版本中配置的 fail_severity，否则回落到常量映射。"""
    if outcome == RESULT_OUTCOME_NORMAL:
        return ""
    return item.get("fail_severity") or RESULT_SEVERITY_BY_OUTCOME[outcome]
