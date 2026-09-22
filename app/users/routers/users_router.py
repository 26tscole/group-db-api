from fastapi import APIRouter, Request
from app.users.models import User
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/users", tags=["users"])

user_crud = CRUDBase[User, schema.UserCreate, schema.UserUpdate](
    User, not_found_detail="User not found"
)


# search users
@router.get("/", response_model=list[schema.UserResponse])
async def search_users(request: Request, db: db_dependency):
    filters = build_filters(User, request.query_params)
    return user_crud.search(db, filters)


# create a new user
@router.post("/", response_model=schema.UserResponse)
async def create_user(user: schema.UserCreate, db: db_dependency):
    return user_crud.create(db, user)


# update the user matching the query filters, e.g. /users/?user_id=1
@router.patch("/", response_model=schema.UserResponse)
async def update_user(request: Request, user: schema.UserUpdate, db: db_dependency):
    filters = user_crud.require_filters(build_filters(User, request.query_params))
    db_user = user_crud.get_by(db, **filters)
    return user_crud.update(db, db_user, user)


# delete user(s) matching the query filters, e.g. /users/?user_id=2
@router.delete("/", response_model=list[schema.UserResponse])
async def delete_users(request: Request, db: db_dependency):
    filters = user_crud.require_filters(build_filters(User, request.query_params))
    db_users = user_crud.get_many_by(db, **filters)
    return user_crud.delete_many(db, db_users)


# delete all users
@router.delete("/all", response_model=list[schema.UserResponse])
async def delete_all_users(db: db_dependency):
    return user_crud.delete_all(db)
