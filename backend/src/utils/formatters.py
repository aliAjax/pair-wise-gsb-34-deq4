def audit_target(kind, id):
    return f"{kind}#{id}"


def checklist_version_label(version_no):
    return f"v{version_no}" if version_no is not None else "-"


def rectify_status_text(status):
    return {"OPEN": "未关闭", "CLOSED": "已关闭"}.get(status, status)


def result_status_text(status):
    return {"PENDING": "待判定", "NORMAL": "正常", "ABNORMAL": "异常"}.get(status, status)
