"""清单版本化 / 任务固定版本 / 隐患合并 的端到端测试。"""
import threading

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.repositories.bootstrap import bootstrap
from src.services.checklist_version_service import ChecklistVersionService
from src.services.inspection_task_service import InspectionTaskService
from src.types.inspection_task_payload import InspectionTaskCreatePayload
from src.utils.audit import reset_audit, list_audit


@pytest.fixture
def client():
    bootstrap()
    reset_audit()
    return TestClient(app)


def _hydrant_task_in_progress():
    service = InspectionTaskService()
    for task in service.list():
        if task["task_type"] == "HYDRANT" and task["status"] == "IN_PROGRESS":
            return task
    raise AssertionError("种子数据缺少进行中的消火栓任务")


def test_seed_keeps_existing_tasks_on_published_v1(client):
    task = _hydrant_task_in_progress()
    assert task["checklist_version"] == "1.0.0"
    assert len(task["checklist_snapshot"]) == 3


def test_publishing_v2_does_not_swap_items_of_claimed_task(client):
    task_before = _hydrant_task_in_progress()
    published = client.post("/api/checklist-version/2/publish", params={"actor_id": 7}).json()
    assert published["status"] == "PUBLISHED"
    assert published["version"] == "2.0.0"

    task_after = client.get(f"/api/inspection-task/{task_before['id']}").json()
    # 已领取任务仍固定 v1，阈值规则没有被 v2 换掉
    assert task_after["checklist_version"] == "1.0.0"
    pressure = next(i for i in task_after["checklist_snapshot"] if i["item_code"] == "HYD-PRESSURE")
    assert pressure["rule"]["min"] == 0.15


def test_submit_grades_with_pinned_version_even_after_new_release(client):
    task = _hydrant_task_in_progress()
    client.post("/api/checklist-version/2/publish")

    # 0.20 在 v1(min=0.15) 下正常，在 v2(min=0.25) 下异常；任务固定 v1，故应判正常
    payload = {
        "actor_id": 1,
        "results": [
            {"item_code": "HYD-PRESSURE", "measured_value": "0.20", "device_id": 1},
            {"item_code": "HYD-LEAK", "measured_value": "无渗漏", "device_id": 1},
            {"item_code": "HYD-ACCESS", "measured_value": "畅通", "device_id": 1},
        ],
    }
    body = client.post(f"/api/inspection-task/{task['id']}/submit", json=payload).json()
    assert {r["item_code"]: r["outcome"] for r in body["results"]} == {
        "HYD-PRESSURE": "NORMAL",
        "HYD-LEAK": "NORMAL",
        "HYD-ACCESS": "NORMAL",
    }
    assert all(r["checklist_version"] == "1.0.0" for r in body["results"])
    assert body["hazard_tickets"] == []
    assert body["task"]["status"] == "SUBMITTED"
    assert body["task"]["finished_at"]


def test_abnormal_result_creates_hazard_per_device(client):
    task = _hydrant_task_in_progress()
    payload = {
        "results": [
            # 0.10 低于 v1 下限 0.15，判异常，fail_severity=HIGH
            {"item_code": "HYD-PRESSURE", "measured_value": "0.10", "device_id": 1},
            {"item_code": "HYD-LEAK", "measured_value": "无渗漏", "device_id": 1},
            {"item_code": "HYD-ACCESS", "measured_value": "畅通", "device_id": 1},
        ]
    }
    body = client.post(f"/api/inspection-task/{task['id']}/submit", json=payload).json()
    assert len(body["hazard_tickets"]) == 1
    ticket = body["hazard_tickets"][0]
    assert ticket["device_id"] == 1
    assert ticket["severity"] == "HIGH"
    assert ticket["found_count"] == 1
    assert ticket["rectify_status"] in ("OPEN", "RECTIFYING", "REVIEWING")


def test_same_device_open_hazard_is_merged_and_counted(client):
    task = _hydrant_task_in_progress()

    def abnormal_submit(measured):
        return client.post(
            f"/api/inspection-task/{task['id']}/submit",
            json={"results": [{"item_code": "HYD-PRESSURE", "measured_value": measured,
                               "device_id": 1}]},
        )

    first = abnormal_submit("0.10")
    assert first.status_code == 200
    ticket_id = first.json()["hazard_tickets"][0]["id"]

    # 首次提交后任务已 SUBMITTED，再次提交会被拒绝；直接构造新任务走服务层触发合并
    client.post("/api/checklist-version/2/publish")
    second_task = client.post("/api/inspection-task", json={
        "building_id": 1, "inspector_id": 1, "plan_date": "2026-10-02",
        "task_type": "HYDRANT", "created_by": 1,
    }).json()
    # 新任务固定的是 v2，0.24 在 v2(min=0.25) 下同样异常，用于验证合并
    second = client.post(f"/api/inspection-task/{second_task['id']}/submit", json={
        "results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.24", "device_id": 1}],
    }).json()
    assert len(second["hazard_tickets"]) == 1
    merged = second["hazard_tickets"][0]
    assert merged["id"] == ticket_id
    assert merged["found_count"] == 2
    assert merged["latest_result_id"] != merged["first_result_id"]
    assert ticket_id in second["merged_hazard_ids"]


def test_hazard_for_different_devices_are_not_merged(client):
    task = _hydrant_task_in_progress()
    body = client.post(f"/api/inspection-task/{task['id']}/submit", json={
        "results": [
            {"item_code": "HYD-PRESSURE", "measured_value": "0.10", "device_id": 1},
            {"item_code": "HYD-LEAK", "measured_value": "有渗漏", "device_id": 2},
        ],
    }).json()
    devices = {h["device_id"] for h in body["hazard_tickets"]}
    assert devices == {1, 2}
    assert all(h["found_count"] == 1 for h in body["hazard_tickets"])


def test_closed_hazard_does_not_merge_new_ticket(client):
    task = _hydrant_task_in_progress()
    first = client.post(f"/api/inspection-task/{task['id']}/submit", json={
        "results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.10", "device_id": 1}],
    }).json()
    ticket_id = first["hazard_tickets"][0]["id"]
    closed = client.post(f"/api/hazard-ticket/{ticket_id}/close",
                         params={"actor_id": 9, "note": "复验合格"}).json()
    assert closed["rectify_status"] == "CLOSED"
    assert closed["closed_at"]

    second_task = client.post("/api/inspection-task", json={
        "building_id": 1, "inspector_id": 1, "plan_date": "2026-10-03",
        "task_type": "HYDRANT", "created_by": 1,
    }).json()
    second = client.post(f"/api/inspection-task/{second_task['id']}/submit", json={
        "results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.10", "device_id": 1}],
    }).json()
    assert len(second["hazard_tickets"]) == 1
    assert second["hazard_tickets"][0]["id"] != ticket_id
    assert second["hazard_tickets"][0]["found_count"] == 1


def test_new_task_pins_latest_published_version(client):
    client.post("/api/checklist-version/2/publish")
    created = client.post("/api/inspection-task", json={
        "building_id": 1, "inspector_id": 2, "plan_date": "2026-10-01",
        "task_type": "HYDRANT", "created_by": 3,
    }).json()
    assert created["checklist_version"] == "2.0.0"
    pressure = next(i for i in created["checklist_snapshot"] if i["item_code"] == "HYD-PRESSURE")
    assert pressure["rule"]["min"] == 0.25


def test_create_task_without_published_version_is_rejected(client):
    resp = client.post("/api/inspection-task", json={
        "building_id": 1, "inspector_id": 2, "plan_date": "2026-10-01",
        "task_type": "SMOKE_DETECTOR", "created_by": 3,
    })
    assert resp.status_code == 409
    assert resp.json()["code"] == "CHECKLIST_NO_PUBLISHED_VERSION"


def test_submit_rejects_item_not_in_pinned_version(client):
    task = _hydrant_task_in_progress()
    client.post("/api/checklist-version/2/publish")
    resp = client.post(f"/api/inspection-task/{task['id']}/submit", json={
        "results": [{"item_code": "NEW-ITEM-FROM-V3", "measured_value": "x"}],
    })
    assert resp.status_code == 422
    assert resp.json()["code"] == "RESULT_ITEM_UNKNOWN"


def test_resubmit_is_rejected_after_completion(client):
    task = _hydrant_task_in_progress()
    payload = {"results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.10",
                            "device_id": 1}]}
    assert client.post(f"/api/inspection-task/{task['id']}/submit", json=payload).status_code == 200
    again = client.post(f"/api/inspection-task/{task['id']}/submit", json=payload)
    assert again.status_code == 409
    assert again.json()["code"] == "TASK_NOT_SUBMITTABLE"


def test_publish_archives_old_version_and_is_traceable(client):
    client.post("/api/checklist-version/2/publish", params={"actor_id": 7})
    versions = {v["version"]: v["status"] for v in client.get("/api/checklist-version").json()}
    assert versions == {"1.0.0": "ARCHIVED", "2.0.0": "PUBLISHED"}

    logs = client.get("/api/audit-log").json()
    actions = {log["action"] for log in logs}
    assert "ChecklistVersion.publish" in actions
    assert "ChecklistVersion.archive" in actions
    publish_log = next(log for log in logs if log["action"] == "ChecklistVersion.publish")
    assert publish_log["actor_id"] == 7
    assert publish_log["detail"]["archived_versions"] == ["1.0.0"]


def test_task_completion_and_hazard_merge_are_traceable(client):
    task = _hydrant_task_in_progress()
    client.post(f"/api/inspection-task/{task['id']}/submit", json={
        "results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.10", "device_id": 1}],
    })
    client.post("/api/checklist-version/2/publish")
    second_task = client.post("/api/inspection-task", json={
        "building_id": 1, "inspector_id": 1, "plan_date": "2026-10-02",
        "task_type": "HYDRANT", "created_by": 1,
    }).json()
    client.post(f"/api/inspection-task/{second_task['id']}/submit", json={
        "results": [{"item_code": "HYD-PRESSURE", "measured_value": "0.24", "device_id": 1}],
    })
    logs = client.get("/api/audit-log").json()
    actions = {log["action"] for log in logs}
    assert "InspectionTask.submit" in actions
    assert "InspectionResult.grade" in actions
    assert "HazardTicket.create" in actions
    assert "HazardTicket.merge" in actions
    merge_log = next(log for log in logs if log["action"] == "HazardTicket.merge")
    assert merge_log["detail"]["found_count"] == 2
    assert merge_log["detail"]["previous_found_count"] == 1


def test_only_draft_can_be_published(client):
    client.post("/api/checklist-version/2/publish")
    again = client.post("/api/checklist-version/2/publish")
    assert again.status_code == 409
    assert again.json()["code"] == "CHECKLIST_NOT_PUBLISHABLE"


def test_simultaneous_publish_notices_creator():
    """发布与建任务同一时刻发生：新任务采用刚发布的版本并带提示。"""
    bootstrap()
    reset_audit()
    checklist_service = ChecklistVersionService()
    task_service = InspectionTaskService()

    moment = "2026-09-29T09:00:00.000Z"
    published = checklist_service.publish(2, actor_id=7, published_at=moment)
    created = task_service.create(
        InspectionTaskCreatePayload(building_id=1, inspector_id=2,
                                    plan_date="2026-10-01", task_type="HYDRANT", created_by=3),
        created_at=moment,
    )
    assert published["version"] == "2.0.0"
    assert created["checklist_version"] == "2.0.0"
    assert "2.0.0" in created["version_notice"]

    pin_log = next(
        log for log in list_audit()
        if log["action"] == "InspectionTask.pin_checklist"
    )
    assert pin_log["detail"]["simultaneous_publish"] is True


def test_concurrent_publish_and_task_creation_always_pins_a_published_version(client):
    """发布与一批建任务并发：每个任务都固定到某个已发布版本，不会落空或损坏。"""
    barrier = threading.Barrier(5)
    results = []
    errors = []

    def create_task(index):
        barrier.wait()
        try:
            resp = client.post("/api/inspection-task", json={
                "building_id": 1, "inspector_id": index, "plan_date": "2026-10-05",
                "task_type": "HYDRANT", "created_by": index,
            })
            results.append(resp.json())
        except Exception as exc:  # noqa: BLE001 - 并发测试需记录线程内异常
            errors.append(exc)

    def publish():
        barrier.wait()
        client.post("/api/checklist-version/2/publish", params={"actor_id": 7})

    threads = [threading.Thread(target=create_task, args=(i,)) for i in range(1, 5)]
    threads.append(threading.Thread(target=publish))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors
    assert len(results) == 4
    for task in results:
        assert task["checklist_version"] in ("1.0.0", "2.0.0")
        assert task["checklist_snapshot"]
