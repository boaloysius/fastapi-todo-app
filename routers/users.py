from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from fastapi import Depends, HTTPException, Path, APIRouter

from models import Todos, Users
from database import SessionLocal
from .auth import get_current_user, bcryptContext

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get("id")).first()


class UpdatePasswordRequest(BaseModel):
    password: str = Field(min_length=6)


@router.patch("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    update_password_request: UpdatePasswordRequest,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    userModel = db.query(Users).filter(Users.id == user.get("id")).first()

    if userModel is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    userModel.hashed_password = bcryptContext.hash(update_password_request.password)

    db.add(userModel)
    db.commit()
