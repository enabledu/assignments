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


@app.post("/assignment/{assignment_id}/edit/")
async def edit_assignment(assignment: AssignmentUpdate) -> UUID:
    pass
    # check if the id is valid


@app.delete("/assignment/{assignment_id}/delete/")
async def delete_assignment(assignment_id: UUID):
    pass
    # check if the id is valid

@app.get("/assignment/{assignment_id}/attachments/")
async def get_all_assignment_attachments(assignment_id: UUID):
    pass
    # check if the id is valid


@app.post("assignment/{assignment_id}/attachment/add")
async def add_attachment_to_assignment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/assignment/{assignment_id}/works/")
async def get_all_assignment_works(assignment_id: UUID):
    pass
    # check if the id is valid


@app.post("assignment/{assignment_id}/work/add")
async def add_attachment_to_work_on_assignment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/work/{work_id}/attachments/")
async def get_all_work_attachments(work_id: UUID):
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


@app.post("/work/{work_id}/grade/{new_grade}")
async def update_work_grade(work_id: UUID, new_grade: int):
    pass
    # check if the id is valid


@app.get("attachment/{attachment_id}/")
async def get_attachment(attachment_id: UUID):
    pass
    # check if the id is valid


@app.delete("attachment/{attachment_id}/delete")
async def delete_attachment(attachment_id: UUID):
    pass
    # check if the id is valid


