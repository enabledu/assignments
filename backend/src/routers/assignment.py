from uuid import UUID

from fastapi import UploadFile, APIRouter, Depends, HTTPException

from assignments.backend.src.models import (Assignment, BaseAssignment, Attachment,
                                            Work, AssignmentID, AttachmentID, ErrorModel)
from enabled.backend.src.database import get_client
from assignments.backend.src import queries

from enabled.backend.src.users.users import current_active_user

assignment_router = APIRouter(prefix="/assignment")


@assignment_router.get("/")
async def get_all_assignments(client=Depends(get_client)) -> list[Assignment]:
    return await queries.get_all_assignments(client)


@assignment_router.post("/add/")
async def add_assignment(assignment: BaseAssignment,
                         user=Depends(current_active_user),
                         client=Depends(get_client)) -> AssignmentID:
    return await queries.add_assignment(client, owner_id=user.id, **assignment.dict())


@assignment_router.post("/{assignment_id}/edit/",
                        responses={404: {"model": ErrorModel},
                                   403: {"model": ErrorModel}})
async def edit_assignment(assignment_id: UUID,
                          assignment: BaseAssignment,
                          user=Depends(current_active_user),
                          client=Depends(get_client)) -> AssignmentID:
    # TODO: Find a better way to replace the additional query that gets the assignment owner.
    owner = await queries.get_assignment_owner(client, assignment_id=assignment_id)

    # If th owner is none, the assignment doesn't exist
    if not owner:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    elif not owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only assignment owner can edit it")
    else:
        # TODO: fix clearing unset properties in the request.
        # in the update query, all parameters are optional.
        # But if a property is not set in the request, it is CLEARED in the DB.
        return await queries.update_assignment(client, assignment_id=assignment_id, **assignment.dict())


@assignment_router.delete("/{assignment_id}/delete/",
                          responses={404: {"model": ErrorModel},
                                     403: {"model": ErrorModel}})
async def delete_assignment(assignment_id: UUID,
                            user=Depends(current_active_user),
                            client=Depends(get_client)) -> AssignmentID:
    owner = await queries.get_assignment_owner(client, assignment_id=assignment_id)

    # If th owner is none, the assignment doesn't exist
    if not owner:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    elif not owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only assignment owner can delete it")
    else:
        return await queries.delete_assignment(client, assignment_id=assignment_id)


@assignment_router.get("/{assignment_id}/attachment/",
                       responses={404: {"model": ErrorModel}})
async def get_all_assignment_attachments(assignment_id: UUID,
                                         client=Depends(get_client)) -> list[Attachment]:
    assignment = await queries.get_assignment(client, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    else:
        return await queries.get_all_assignment_attachments(client, assignment_id=assignment_id)


@assignment_router.post("/{assignment_id}/attachment/add/",
                        responses={404: {"model": ErrorModel},
                                   403: {"model": ErrorModel}})
async def add_attachment_to_assignment(assignment_id: UUID,
                                       attachment: UploadFile,
                                       user=Depends(current_active_user),
                                       client=Depends(get_client)) -> AttachmentID:
    owner = await queries.get_assignment_owner(client, assignment_id=assignment_id)

    # If th owner is none, the assignment doesn't exist
    if not owner:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    elif not owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only assignment owner can add attachments to it")
    else:
        file = await attachment.read()
        return await queries.add_attachment_to_assignment(client,
                                                          assignment_id=assignment_id,
                                                          filename=attachment.filename,
                                                          content_type=attachment.content_type,
                                                          file=file)


@assignment_router.get("/{assignment_id}/work/",
                       responses={404: {"model": ErrorModel}})
async def get_all_assignment_works(assignment_id: UUID,
                                   client=Depends(get_client)) -> list[Work]:
    assignment = await queries.get_assignment(client, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    else:
        return await queries.get_all_assignment_works(client, assignment_id=assignment_id)


@assignment_router.post("/{assignment_id}/work/add/",
                        responses={404: {"model": ErrorModel}})
async def add_attachment_to_work_on_assignment(assignment_id: UUID,
                                               attachment: UploadFile,
                                               user=Depends(current_active_user),
                                               client=Depends(get_client)) -> AttachmentID:
    # TODO: find a better way to instantiate or get the work by the user on that specific assignment
    assignment = await queries.get_assignment(client, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    else:
        file = await attachment.read()
        work = await queries.get_work_by_owner_on_assignment(client, owner_id=user.id, assignment_id=assignment_id)
        if not work:
            return await queries.add_work_to_assignment(client,
                                                        owner_id=user.id,
                                                        assignment_id=assignment_id,
                                                        filename=attachment.filename,
                                                        content_type=attachment.content_type,
                                                        file=file)
        else:
            return await queries.add_attachment_to_work(client,
                                                        work_id=work.id,
                                                        filename=attachment.filename,
                                                        content_type=attachment.content_type,
                                                        file=file)


@assignment_router.get("/{assignment_id}/work/me/",
                       responses={404: {"model": ErrorModel}})
async def get_work_on_assignment_by_current_user(assignment_id: UUID,
                                                 user=Depends(current_active_user),
                                                 client=Depends(get_client)) -> Work | None:
    assignment = await queries.get_assignment(client, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment NOT found")
    else:
        return await queries.get_work_by_owner_on_assignment(client, owner_id=user.id, assignment_id=assignment_id)
