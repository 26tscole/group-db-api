from fastapi import APIRouter, Request, HTTPException
from app.users import schema
from app.users.models import User
from app.db_deps import db_dependency
from app.users.security import user_dependency
from app.users.services.users_service import search_users, create_user, update_user, delete_users, delete_all_users


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schema.UserResponse)
async def get_current_user_profile(current_user: user_dependency, db: db_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# search users
@router.get("/", response_model=list[schema.UserResponse])
def get_users(request: Request, db: db_dependency):
    return search_users(request, db)


# create a new user
@router.post("/", response_model=schema.UserResponse)
def post_user(user: schema.UserCreate, db: db_dependency):
    return create_user(user, db)


# update the user matching the query filters, e.g. /users/?user_id=1
@router.patch("/", response_model=schema.UserResponse)
def patch_user(request: Request, user: schema.UserUpdate, db: db_dependency):
    return update_user(request, user, db)


# delete user(s) matching the query filters, e.g. /users/?user_id=2
@router.delete("/", response_model=list[schema.UserResponse])
def delete_users_route(request: Request, db: db_dependency):
    return delete_users(request, db)


# delete all users
@router.delete("/all", response_model=list[schema.UserResponse])
def delete_all_users_route(db: db_dependency):
    return delete_all_users(db)