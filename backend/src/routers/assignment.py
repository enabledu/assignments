from uuid import UUID

from fastapi import UploadFile, APIRouter, Depends

from assignments.backend.src.models import Assignment, BaseAssignment, Attachment, Work, AssignmentID, ErrorModel
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
    # TODO: Handle optional values in EdgeDB query
    return await queries.add_assignment(client, owner_id=user.id, **assignment.dict())


@assignment_router.post("/{assignment_id}/edit/")
async def edit_assignment(assignment_id: UUID,
                          assignment: BaseAssignment,
                          client=Depends(get_client)) -> AssignmentID:
    # TODO: Handle optional values in EdgeDB query

    return await queries.update_assignment(client, assignment_id=assignment_id, **assignment.dict())


@assignment_router.delete("/{assignment_id}/delete/")
async def delete_assignment(assignment_id: UUID,
                            client=Depends(get_client)) -> None:
    pass
    # async for tx in client.transaction():
    #     async with tx:
    #         await tx.execute("INSERT User {name := 'Don'}")


@assignment_router.get("/{assignment_id}/attachments/",
                       responses={404: {"model": ErrorModel}})
async def get_all_assignment_attachments(assignment_id: UUID,
                                         client=Depends(get_client)) -> list[Attachment]:
    return await queries.get_all_assignment_attachments(client, assignment_id=assignment_id)


@assignment_router.post("/{assignment_id}/attachment/add/")
async def add_attachment_to_assignment(assignment_id: UUID,
                                       attachment: UploadFile,
                                       client=Depends(get_client)):
    file = await attachment.read()
    return await queries.add_attachment_to_assignment(client,
                                                      assignment_id=assignment_id,
                                                      filename=attachment.filename,
                                                      content_type=attachment.content_type,
                                                      file=file)


@assignment_router.get("/{assignment_id}/works/")
async def get_all_assignment_works(assignment_id: UUID,
                                   client=Depends(get_client)) -> list[Work]:
    pass
    # check if the id is valid


@assignment_router.post("/{assignment_id}/work/add/")
async def add_attachment_to_work_on_assignment(assignment_id: UUID,
                                               attachment: UploadFile,
                                               client=Depends(get_client)) -> UUID:
    pass
    # check if the id is valid
