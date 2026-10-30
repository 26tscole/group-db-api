from fastapi import APIRouter, Request
from app.users import schema
from app.db_deps import db_dependency
from app.users.services.security_service import user_dependency
from app.users.services.users_service import update_user, get_user


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schema.UserResponse)
async def get_current_user_profile(current_user: user_dependency, db: db_dependency):
    return get_user(current_user, db)


@router.patch("/me", response_model=schema.UserResponse)
def patch_user(
    current_user: user_dependency,
    user: schema.UserUpdate,
    db: db_dependency,
):
    return update_user(current_user, user, db)
