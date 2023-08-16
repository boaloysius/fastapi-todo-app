from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(getDb)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/")
async def readAll(db: dbDependency, status_code=status.HTTP_200_OK):
    return db.query(Todos).all()


@app.get("/todo/{todoId}", status_code=status.HTTP_200_OK)
async def readAll(db: dbDependency, todoId: int = Path(gt=0)):
    todoModel = db.query(Todos).filter(Todos.id == todoId).first()
    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todoModel


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: dbDependency, todoRequest: TodoRequest):
    todoModel = Todos(**todoRequest.model_dump())
    db.add(todoModel)
    db.commit()


@app.put("/todo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: dbDependency, todoRequest: TodoRequest, todoId: int = Path(gt=0)
):
    todoModel = db.query(Todos).filter(Todos.id == todoId).first()
    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todoModel.title = todoRequest.title
    todoModel.description = todoRequest.description
    todoModel.priority = todoRequest.priority
    todoModel.complete = todoRequest.complete

    db.add(todoModel)
    db.commit()


@app.delete("/todo/{todoId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: dbDependency, todoId: int = Path(gt=0)):
    todoModel = db.query(Todos).filter(Todos.id == todoId).first()
    if todoModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todoId).delete()
    db.commit()
