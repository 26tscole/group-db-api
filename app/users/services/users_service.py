from app.users.models import User
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from fastapi import HTTPException
from app.users.routers.security_router import user_dependency

user_crud = CRUDBase[User, schema.createUserRequest, schema.UserUpdate](
    User, not_found_detail="User not found"
)

def get_user(current_user: user_dependency, db: db_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return user_crud.get_by(db, id=current_user["user_id"])

def update_user(current_user: user_dependency, user: schema.UserUpdate, db: db_dependency):
    db_user = user_crud.get_by(db, id=current_user["user_id"])
    return user_crud.update(db, db_user, user)
