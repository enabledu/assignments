from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from apps.assignments.backend.src.routers.assignment import assignment_router
from apps.assignments.backend.src.routers.attachment import attachment_router
from apps.assignments.backend.src.routers.work import work_router

app = APIRouter(tags=["assignments"], prefix="/assignments")

app.include_router(assignment_router)
app.include_router(work_router)
app.include_router(attachment_router)


@app.get("/")
async def read_root():
    return RedirectResponse(url="http://127.0.0.1:8000/assignments/frontend/out/index.html")
