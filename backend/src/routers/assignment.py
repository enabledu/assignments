from uuid import UUID

from fastapi import UploadFile, APIRouter

from apps.assignments.backend.src.models import Assignment, BaseAssignment, Attachment, Work

assignment_router = APIRouter(prefix="/assignment")


@assignment_router.get("/assignment/")
async def get_all_assignments() -> list[Assignment]:
    pass
    # get all the assignments from DB


@assignment_router.post("/assignment/add/")
async def add_assignment(assignment: BaseAssignment) -> UUID:
    pass


@assignment_router.post("/assignment/{assignment_id}/edit/")
async def edit_assignment(assignment_id: UUID, assignment: BaseAssignment) -> None:
    pass
    # check if the id is valid


@assignment_router.delete("/assignment/{assignment_id}/delete/")
async def delete_assignment(assignment_id: UUID) -> None:
    pass
    # check if the id is valid

@assignment_router.get("/assignment/{assignment_id}/attachments/")
async def get_all_assignment_attachments(assignment_id: UUID) -> list[Attachment]:
    pass
    # check if the id is valid


@assignment_router.post("assignment/{assignment_id}/attachment/add")
async def add_attachment_to_assignment(assignment_id: UUID, attachment: UploadFile) -> UUID:
    pass
    # check if the id is valid


@assignment_router.get("/assignment/{assignment_id}/works/")
async def get_all_assignment_works(assignment_id: UUID) -> list[Work]:
    pass
    # check if the id is valid


@assignment_router.post("assignment/{assignment_id}/work/add")
async def add_attachment_to_work_on_assignment(assignment_id: UUID, attachment: UploadFile) -> UUID:
    pass
    # check if the id is valid
