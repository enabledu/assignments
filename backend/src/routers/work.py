from uuid import UUID

from fastapi import APIRouter

from apps.assignments.backend.src.models import Attachment

work_router = APIRouter(prefix="/work")


@work_router.get("/work/{work_id}/attachments/")
async def get_all_work_attachments(work_id: UUID) -> list[Attachment]:
    pass
    # check if the id is valid


@work_router.post("/work/{work_id}/submit/")
async def submit_work(assignment_id: UUID) -> None:
    pass
    # check if the id is valid


@work_router.post("/work/{work_id}/unsubmit/")
async def unsubmit_work(work_id: UUID) -> None:
    pass
    # check if the id is valid


@work_router.post("/work/{work_id}/grade/{new_grade}")
async def update_work_grade(work_id: UUID, new_grade: int) -> None:
    pass
    # check if the id is valid
