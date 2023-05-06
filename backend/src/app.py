from uuid import UUID

from fastapi import APIRouter, UploadFile
from fastapi.responses import RedirectResponse

from apps.assignments.backend.src.models import AssignmentAdd, AssignmentUpdate, BaseAssignment

app = APIRouter(tags=["assignments"], prefix="/assignments")


@app.get("/")
async def read_root():
    return RedirectResponse(url="http://127.0.0.1:8000/assignments/frontend/out/index.html")


@app.get("/assignment/")
async def get_assignment() -> BaseAssignment:
    pass
    # get all the assignments from DB


@app.post("/assignment/add/")
async def add_assignment(assignment: AssignmentAdd) -> UUID:
    pass


@app.post("/assignment/{assignment_id}/update/")
async def update_assignment(assignment: AssignmentUpdate) -> UUID:
    pass
    # check if the id is valid


@app.delete("/assignment/{assignment_id}/delete/")
async def delete_assignment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/assignment/{assignment_id}/works/")
async def get_all_assignment_works(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/assignment/{assignment_id}/attachment/")
async def get_all_assignment_attachments(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/assignment/attachment/{attachment_id}/")
async def get_assignment_attachment(attachment_id: UUID):
    pass
    # check if the id is valid

@app.post("assignment/{assignment_id}/work/attachment")
async def add_attachment_to_work_on_assignment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/work/{work_id}/")
async def get_work(work_id: UUID):
    pass
    # check if the id is valid


@app.get("/work/{work_id}/attachment/")
async def get_all_work_attachments(work_id: UUID):
    pass
    # check if the id is valid


@app.get("/work/attachment/{attachment_id}/")
async def get_all_work_attachments(attachment_id: UUID):
    pass
    # check if the id is valid


@app.post("/work/{work_id}/submit/")
async def submit_work(assignment_id: UUID):
    pass
    # check if the id is valid

@app.post("/work/{work_id}/unsubmit/")
async def unsubmit_work(work_id: UUID):
    pass
    # check if the id is valid


@app.post("/work/{work_id}/grade")
async def update_work_grade(work_id: UUID):
    pass
    # check if the id is valid


# Other way for attachment implementation
@app.get("attachment/{attachment_id}/")
async def get_attachment(attachment_id: UUID):
    pass
    # check if the id is valid


@app.delete("attachment/{attachment_id}/delete")
async def delete_attachment(attachment_id: UUID):
    pass
    # check if the id is valid


