from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Body, UploadFile
from fastapi.responses import RedirectResponse


app = APIRouter(tags=["assignments"], prefix="/assignments")


@app.get("/")
async def read_root():
    return RedirectResponse(url="http://127.0.0.1:8000/assignments/frontend/out/index.html")


@app.get("/assignment/")
async def get_assignment(assignment_id: UUID = None):
    if assignment_id == None:
        pass
        # get all the assignments from DB
    else:
        pass
        # get the specific assignment
        # if the id is not valid ...


@app.post("/assignment/add/")
async def add_assignment(title: str = Body(),
                         deadline: datetime = Body(None),
                         description: str = Body(None),
                         max_grade: int = Body(None)):
    pass


@app.post("/assignment/{assignment_id}/update/")
async def update_assignment(assignment_id: UUID,
                            title: str = Body(),
                            description: str = Body(None),
                            max_grade: int = Body(None)):
    pass
    # check if the id is valid


@app.delete("/assignment/{assignment_id}/delete/")
async def delete_assignment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.get("/assignment/{assignment_id}/work/")
async def get_works_ids(assignment_id: UUID):
    pass
    # check if the id is valid


@app.post("/assignment/{assignment_id}/work/add/")
async def submit_work(assignment_id: UUID):
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


@app.post("/assignment/{assignment_id}/attachment/add/")
async def add_assignment_attachment(assignment_id: UUID):
    pass
    # check if the id is valid


@app.delete("/assignment/attachment/{attachment_id}/delete/")
async def delete_assignment_attachment(attachment_id: UUID):
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


@app.post("/work/{work_id}/unsubmit/")
async def unsubmit_work(work_id: UUID):
    pass
    # check if the id is valid


@app.post("/work/{work_id}/attachment/add/")
async def add_work_attachment(work_id: UUID):
    pass
    # check if the id is valid


@app.delete("/work/attachment/{attachment_id}/delete/")
async def delete_attachment(attachment_id: UUID):
    pass
    # check if the id is valid


@app.post("/work/{work_id}/grade/add/")
async def add_work_grade(work_id: UUID):
    pass
    # check if the id is valid


@app.post("/work/{work_id}/grade/update/")
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


