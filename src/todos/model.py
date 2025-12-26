from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.entities.todo import Priority

class TodoBase(BaseModel):
    title: str
    description: str
    priority: Priority = Priority.MEDIUM

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: UUID
    completed: bool
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)