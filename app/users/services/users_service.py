from app.users.models import User
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from fastapi import HTTPException

user_crud = CRUDBase[User, schema.createUserRequest, schema.UserUpdate](
    User, not_found_detail="User not found"
)

def get_user(current_user: dict, db: db_dependency):
    return user_crud.get_by(db, id=current_user["user_id"])

def update_user(current_user: dict, user: schema.UserUpdate, db: db_dependency):
    db_user = user_crud.get_by(db, id=current_user["user_id"])
    return user_crud.update(db, db_user, user)
