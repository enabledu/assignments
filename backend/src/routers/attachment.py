from uuid import UUID

from fastapi import APIRouter, Depends

from enabled.backend.src.database import get_client
from assignments.backend.src import queries

attachment_router = APIRouter(prefix="/attachment")


@attachment_router.get("attachment/{attachment_id}/")
async def get_attachment(attachment_id: UUID,
                         client=Depends(get_client)) -> bytes:
    pass
    # check if the id is valid


@attachment_router.delete("attachment/{attachment_id}/delete")
async def delete_attachment(attachment_id: UUID,
                            client=Depends(get_client)) -> None:
    pass
    # check if the id is valid
