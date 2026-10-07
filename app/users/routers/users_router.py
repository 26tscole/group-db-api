from fastapi import APIRouter, Request
from app.users import schema
from app.dependencies import db_dependency
from app.users.services.users_service import search_users, create_user, update_user, delete_users, delete_all_users


router = APIRouter(prefix="/users", tags=["users"])

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