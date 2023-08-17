from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException, Path, APIRouter

from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/")
async def read_all(
    user: user_dependency, db: db_dependency, status_code=status.HTTP_200_OK
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/{todoId}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todoId: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = (
        db.query(Todos)
        .filter(Todos.id == todoId)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todoModel


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todoRequest: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = Todos(**todoRequest.model_dump(), owner_id=user.get("id"))
    db.add(todoModel)
    db.commit()


@router.put("/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todoRequest: TodoRequest,
    todoId: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"))
        .filter(Todos.id == todoId)
        .first()
    )
    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todoModel.title = todoRequest.title
    todoModel.description = todoRequest.description
    todoModel.priority = todoRequest.priority
    todoModel.complete = todoRequest.complete

    db.add(todoModel)
    db.commit()


@router.delete("/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todoId: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todoModel = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"))
        .filter(Todos.id == todoId)
        .first()
    )

    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todoId).filter(
        Todos.owner_id == user.get("id")
    ).delete()

    db.commit()
