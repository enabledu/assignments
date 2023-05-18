from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from assignments.backend.src.models import Attachment, WorkID, ErrorModel
from enabled.backend.src.database import get_client
from assignments.backend.src import queries

from enabled.backend.src.users.users import current_active_user

from enabled.backend.src.users.db import User

work_router = APIRouter(prefix="/work")


@work_router.get("/{work_id}/attachment/",
                 responses={404: {"model": ErrorModel}})
async def get_all_work_attachments(work_id: UUID,
                                   client=Depends(get_client)) -> list[Attachment]:
    work = await queries.get_work(client, work_id=work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Work NOT found")
    else:
        return await queries.get_all_work_attachments(client, work_id=work_id)


@work_router.post("/{work_id}/submit/",
                  responses={404: {"model": ErrorModel},
                             403: {"model": ErrorModel}})
async def submit_work(work_id: UUID,
                      user: User = Depends(current_active_user),
                      client=Depends(get_client)) -> WorkID:
    work = await queries.get_work(client, work_id=work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Work NOT found")
    elif not work.owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only work owner can submit their work")
    else:
        return await queries.submit_work(client, work_id=work_id)


@work_router.post("/{work_id}/unsubmit/",
                  responses={404: {"model": ErrorModel},
                             403: {"model": ErrorModel}})
async def unsubmit_work(work_id: UUID,
                        user: User = Depends(current_active_user),
                        client=Depends(get_client)) -> WorkID:
    work = await queries.get_work(client, work_id=work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Work NOT found")
    elif not work.owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only work owner can unsubmit their work")
    else:
        return await queries.unsubmit_work(client, work_id=work_id)


@work_router.post("/{work_id}/grade/{new_grade}",
                  responses={404: {"model": ErrorModel},
                             403: {"model": ErrorModel}})
async def update_work_grade(work_id: UUID,
                            new_grade: int,
                            user: User = Depends(current_active_user),
                            client=Depends(get_client)) -> WorkID:
    # TODO: find a better way to update the grade with more efficient queries.
    assignment = await queries.get_assignment_of_work(client, work_id=work_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Work NOT found")
    elif not assignment.owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only assignment owner can grade its work")
    else:
        return await queries.grade_work(client, work_id=work_id, grade=new_grade)
