from fastapi import APIRouter

from src.controllers.checklist_version_controller import (
    create_checklist_draft,
    get_current_checklist,
    list_checklist_version,
    publish_checklist,
)

router = APIRouter(prefix="/api/checklist-version", tags=["ChecklistVersion"])
router.get("")(list_checklist_version)
router.get("/current/{task_type}")(get_current_checklist)
router.post("/draft")(create_checklist_draft)
router.post("/{version_id}/publish")(publish_checklist)
