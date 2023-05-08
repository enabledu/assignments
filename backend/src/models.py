from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    detail: str


class Owner(BaseModel):
    id: UUID
    username: str


class AssignmentID(BaseModel):
    id: UUID


class BaseAssignment(BaseModel):
    title: str = Field(max_length=100)
    deadline: datetime = None
    description: str = None
    max_grade: int = Field(default=0, ge=0)


class Assignment(BaseAssignment, AssignmentID):
    owner: Owner


class WorkID(BaseModel):
    id: UUID


class BaseWork(BaseModel):
    is_submitted: bool
    grade: int


class Work(BaseWork, WorkID):
    owner: Owner


class AttachmentID(BaseModel):
    id: UUID


class Attachment(AttachmentID):
    filename: str
    content_type: str


class AttachmentFile(BaseModel):
    file: bytes
