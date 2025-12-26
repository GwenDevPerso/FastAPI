from fastapi import APIRouter, status
from typing import List
from uuid import UUID
from . import model, service
from ..auth.service import CurrentUser
from ..database.core import DbSession

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=model.TodoResponse)
async def create_todo(todo: model.TodoCreate, current_user: CurrentUser, db: DbSession):
    return service.create_todo(current_user, db, todo)

@router.get("/", response_model=List[model.TodoResponse])
async def get_todos(current_user: CurrentUser, db: DbSession):
    return service.get_todos(current_user, db)

@router.get("/{todo_id}", response_model=model.TodoResponse)
async def get_todo_by_id(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    return service.get_todo_by_id(current_user, db, todo_id)

@router.put("/{todo_id}", status_code=status.HTTP_200_OK, response_model=model.TodoResponse)
async def update_todo(todo_id: UUID, todo: model.TodoCreate, current_user: CurrentUser, db: DbSession):
    return service.update_todo(current_user, db, todo_id, todo)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    return service.delete_todo(current_user, db, todo_id)

@router.put("/{todo_id}/complete", status_code=status.HTTP_200_OK, response_model=model.TodoResponse)
async def complete_todo(todo_id: UUID, current_user: CurrentUser, db: DbSession):
    return service.complete_todo(current_user, db, todo_id)
