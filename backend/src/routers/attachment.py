from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from enabled.backend.src.database import get_client
from assignments.backend.src import queries

from assignments.backend.src.models import AttachmentFile, AttachmentID, ErrorModel

attachment_router = APIRouter(prefix="/attachment")


@attachment_router.get("/{attachment_id}/",
                       response_class=PlainTextResponse,
                       responses={404: {"model": ErrorModel}})
async def get_attachment(attachment_id: UUID,
                         client=Depends(get_client)) -> bytes:
    attachment_file = await queries.get_attachment(client, attachment_id=attachment_id)
    if attachment_file:
        return attachment_file.file
    else:
        raise HTTPException(status_code=404, detail="Attachment NOT found")


@attachment_router.delete("/{attachment_id}/delete", responses={404: {"model": ErrorModel}})
async def delete_attachment(attachment_id: UUID,
                            client=Depends(get_client)) -> AttachmentID:
    result = await queries.delete_attachment(client, attachment_id=attachment_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Attachment NOT found")
