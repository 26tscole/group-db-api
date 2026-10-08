from datetime import datetime, timedelta
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from app.dependencies import db_dependency
from app.users.models import User
from app.users.schema import TokenData, createUserRequest
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# To change the algorithm, swap the hasher here (e.g. BcryptHasher()).
password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: createUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=hash_password(create_user_request.password),
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        date_of_birth=create_user_request.date_of_birth,
        phone_number=create_user_request.phone_number,
        email=create_user_request.email,
        address=create_user_request.address
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model

@router.post("/token", response_model=TokenData)
async def login_for_access_token(
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user