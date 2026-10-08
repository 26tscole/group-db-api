from app.users.models import User
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from fastapi import Request

user_crud = CRUDBase[User, schema.UserCreate, schema.UserUpdate](
    User, not_found_detail="User not found"
)

def search_users(request: Request, db: db_dependency):
    filters = build_filters(User, request.query_params)
    return user_crud.search(db, filters)

def create_user(user: schema.UserCreate, db: db_dependency):
    return user_crud.create(db, user)

def update_user(request: Request, user: schema.UserUpdate, db: db_dependency):
    filters = user_crud.require_filters(build_filters(User, request.query_params))
    db_user = user_crud.get_by(db, **filters)
    return user_crud.update(db, db_user, user)

def delete_users(request: Request, db: db_dependency):
    filters = user_crud.require_filters(build_filters(User, request.query_params))
    db_users = user_crud.get_many_by(db, **filters)
    return user_crud.delete_many(db, db_users)

def delete_all_users(db: db_dependency):
    return user_crud.delete_all(db)
