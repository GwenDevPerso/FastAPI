from datetime import datetime, timezone
from fastapi import HTTPException
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from . import model
from src.auth.model import TokenData
from src.entities.todo import Todo
from src.exceptions import TodoNotFoundError, TodoCreationError
import logging


def create_todo(current_user: TokenData, db: Session, todo: model.TodoCreate) -> Todo:
    try:
        new_todo = Todo(**todo.model_dump())
        new_todo.user_id = current_user.get_uuid()
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        logging.info(f"Todo created successfully for user {current_user.get_uuid()}")
        return new_todo
    except Exception as e:
        logging.error(f"Error creating todo: {e}")
        raise TodoCreationError(f"Error creating todo: {e}")

def get_todos(current_user: TokenData, db: Session) -> list[model.TodoResponse]:
    try:
        todos = db.query(Todo).filter(Todo.user_id == current_user.get_uuid()).all()
        logging.info(f"Todos retrieved successfully for user {current_user.get_uuid()}")
        return todos
    except Exception as e:
        logging.error(f"Error getting todos: {e}")
        raise TodoNotFoundError(f"Error getting todos: {e}")

def get_todo_by_id(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == current_user.get_uuid()).first()
        if not todo:
            logging.warning(f"Todo with id {todo_id} not found for user {current_user.get_uuid()}")
            raise TodoNotFoundError(f"Todo with id {todo_id} not found for user {current_user.get_uuid()}")
        logging.info(f"Todo retrieved successfully for user {current_user.get_uuid()}")
        return todo
    except Exception as e:
        logging.error(f"Error getting todo by id: {e}")
        raise TodoNotFoundError(f"Error getting todo by id: {e}")

def update_todo(current_user: TokenData, db: Session, todo_id: UUID, todo_update: model.TodoCreate) -> Todo:
    try:
        todo_data = todo_update.model_dump(exclude_unset=True)
        db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == current_user.get_uuid()).update(todo_data)
        db.commit()
        logging.info(f"Todo updated successfully for user {current_user.get_uuid()}")
        return get_todo_by_id(current_user, db, todo_id)
    except Exception as e:
        logging.error(f"Error updating todo: {e}")
        raise TodoNotFoundError(f"Error updating todo: {e}")

def complete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> Todo:
    try:
        todo = get_todo_by_id(current_user, db, todo_id)
        if todo.completed:
            logging.warning(f"Todo with id {todo_id} already completed for user {current_user.get_uuid()}")
            return todo
        todo.completed = True
        todo.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(todo)
        logging.info(f"Todo completed successfully for user {current_user.get_uuid()}")
        return todo
    except Exception as e:
        logging.error(f"Error completing todo: {e}")
        raise TodoNotFoundError(f"Error completing todo: {e}")

def delete_todo(current_user: TokenData, db: Session, todo_id: UUID) -> None:
    try:
        todo = get_todo_by_id(current_user, db, todo_id)
        db.delete(todo)
        db.commit()
        logging.info(f"Todo deleted successfully for user {current_user.get_uuid()}")
    except Exception as e:
        logging.error(f"Error deleting todo: {e}")
        raise TodoNotFoundError(f"Error deleting todo: {e}")