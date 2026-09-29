from fastapi import APIRouter

from src.controllers.checklist_version_controller import (
    list_checklist_version,
    create_checklist_version,
    publish_checklist_version,
)

router = APIRouter(prefix="/api/checklist-version", tags=["ChecklistVersion"])
router.get("")(list_checklist_version)
router.post("/draft")(create_checklist_version)
router.post("/{version_id}/publish")(publish_checklist_version)
