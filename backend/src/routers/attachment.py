from uuid import UUID

from fastapi import APIRouter

attachment_router = APIRouter(prefix="/attachment")


@attachment_router.get("attachment/{attachment_id}/")
async def get_attachment(attachment_id: UUID) -> bytes:
    pass
    # check if the id is valid


@attachment_router.delete("attachment/{attachment_id}/delete")
async def delete_attachment(attachment_id: UUID) -> None:
    pass
    # check if the id is valid
