import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from enabled.backend.src.database import get_client
from assignments.backend.src import queries

from assignments.backend.src.models import AttachmentFile, AttachmentID, ErrorModel
from fastapi.responses import StreamingResponse

from enabled.backend.src.users.users import current_active_user

attachment_router = APIRouter(tags=["assignments: attachment"], prefix="/attachment")


@attachment_router.get("/{attachment_id}/",
                       response_class=StreamingResponse,
                       responses={404: {"model": ErrorModel}})
async def get_attachment(attachment_id: UUID,
                         client=Depends(get_client)):
    attachment_file = await queries.get_attachment(client, attachment_id=attachment_id)
    stream = io.BytesIO(attachment_file.file)
    if attachment_file:
        try:
            attachment_file.filename.encode('latin-1')
        except UnicodeEncodeError:
            return StreamingResponse(stream,
                                     media_type=attachment_file.content_type,
                                     headers={
                                         "Content-Disposition": f'attachment; filename*=utf-8"{attachment_file.filename.encode()}'})
        else:
            return StreamingResponse(stream,
                                     media_type=attachment_file.content_type,
                                     headers={
                                         "Content-Disposition": f"attachment; filename={attachment_file.filename}"})
    else:
        raise HTTPException(status_code=404, detail="Attachment NOT found")


@attachment_router.delete("/{attachment_id}/delete",
                          responses={404: {"model": ErrorModel},
                                     403: {"model": ErrorModel}})
async def delete_attachment(attachment_id: UUID,
                            user=Depends(current_active_user),
                            client=Depends(get_client)) -> AttachmentID:
    # TODO: find a better way to make sure the attachment exists
    owner = await queries.get_attachment_owner(client, attachment_id=attachment_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Attachment NOT found")
    elif not owner.id == user.id:
        raise HTTPException(status_code=403, detail="Only attachment owner can delete it")
    else:
        return await queries.delete_attachment(client, attachment_id=attachment_id)

