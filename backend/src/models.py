from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseAssignment(BaseModel):
    title: str = Field(max_length=100)
    deadline: datetime = None
    description: str
    max_grade: int = Field(gt=0)


class Assignment(BaseAssignment):
    assignment_id: UUID


class BaseWork(BaseModel):
    # owner: str
    is_submitted: bool
    grade: int


class Work(BaseWork):
    work_id: UUID


class Attachment(BaseModel):
    filename: str
    content_type: str
