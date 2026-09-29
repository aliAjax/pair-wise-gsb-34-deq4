from fastapi import APIRouter
from src.controllers.inspection_task_controller import (
    create_inspection_task,
    get_inspection_task,
    list_inspection_task,
    submit_inspection_task,
)

router = APIRouter(prefix="/api/inspection-task", tags=["InspectionTask"])
router.get("")(list_inspection_task)
router.get("/{task_id}")(get_inspection_task)
router.post("")(create_inspection_task)
router.post("/{task_id}/submit")(submit_inspection_task)
