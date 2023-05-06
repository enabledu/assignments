from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class BaseAssignment(BaseModel):
    title: str = Field(max_length=100)
    deadline: datetime = None
    description: str
    max_grade: int = Field(gt=0)


class AssignmentAdd(BaseAssignment):
    pass


class AssignmentUpdate(BaseAssignment):
    assignment_id: UUID
