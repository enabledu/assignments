from uuid import UUID

from fastapi import APIRouter, Depends

from assignments.backend.src.models import Attachment
from enabled.backend.src.database import get_client
from assignments.backend.src import queries

work_router = APIRouter(prefix="/work")


@work_router.get("/{work_id}/attachments/")
async def get_all_work_attachments(work_id: UUID,
                                   client=Depends(get_client)) -> list[Attachment]:
    pass
    # check if the id is valid


@work_router.post("/{work_id}/submit/")
async def submit_work(assignment_id: UUID,
                      client=Depends(get_client)) -> None:
    pass
    # check if the id is valid


@work_router.post("/{work_id}/unsubmit/")
async def unsubmit_work(work_id: UUID,
                        client=Depends(get_client)) -> None:
    pass
    # check if the id is valid


@work_router.post("/{work_id}/grade/{new_grade}")
async def update_work_grade(work_id: UUID,
                            new_grade: int,
                            client=Depends(get_client)) -> None:
    pass
    # check if the id is valid
