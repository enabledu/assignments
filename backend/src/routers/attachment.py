import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from enabled.backend.src.database import get_client
from assignments.backend.src import queries

from assignments.backend.src.models import AttachmentFile, AttachmentID, ErrorModel
from fastapi.responses import StreamingResponse

attachment_router = APIRouter(prefix="/attachment")


@attachment_router.get("/{attachment_id}/",
                       response_class=StreamingResponse,
                       responses={404: {"model": ErrorModel}})
async def get_attachment(attachment_id: UUID,
                         client=Depends(get_client)):
    attachment_file = await queries.get_attachment(client, attachment_id=attachment_id)
    stream = io.BytesIO(attachment_file.file)
    if attachment_file:
        return StreamingResponse(stream,
                                 media_type=attachment_file.content_type,
                                 headers={"Content-Disposition": f"attachment; filename={attachment_file.filename}"})
    else:
        raise HTTPException(status_code=404, detail="Attachment NOT found")


@attachment_router.delete("/{attachment_id}/delete",
                          responses={404: {"model": ErrorModel}})
async def delete_attachment(attachment_id: UUID,
                            client=Depends(get_client)) -> AttachmentID:
    result = await queries.delete_attachment(client, attachment_id=attachment_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Attachment NOT found")
