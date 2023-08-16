from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

from models import Users

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "15e7cdbb99fa95565d303adac93e228c2c3cfb757daec213bfdcbdd92cf50dd1"
ALGORITHM = "HS256"

bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(getDb)]


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticateUser(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False

    if not bcryptContext.verify(password, user.hashed_password):
        return False

    return user


def createAccessToken(username: str, userId: int, expiresDelta: timedelta):
    encode = {"sub": username, "id": userId}
    expires = datetime.utcnow() + expiresDelta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def getCurrentUser(token: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        userId: int = payload.get("id")
        if username is None or userId is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": userId}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        ) from e


@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(db: dbDependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcryptContext.hash(create_user_request.password),
        is_active=True,
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def loginForAccessToken(
    formData: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDependency
):
    user = authenticateUser(formData.username, formData.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )
    token = createAccessToken(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
