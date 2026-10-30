from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from app.db_deps import db_dependency
from app.users.schema import createUserRequest
from app.users.services import security_service as svc

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: createUserRequest):
    return svc.create_user(db, create_user_request)

@router.post("/token")
async def login_for_access_token(
    response: Response,
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = svc.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    svc.set_auth_cookie(response, svc.create_access_token(user.username, user.id))
    return {"message": "Logged in"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}
