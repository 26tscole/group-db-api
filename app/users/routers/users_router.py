from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from app.users.models import User
from app.users import schema
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def find_user_by_id(user_id: int, db: db_dependency) -> User:
    result = db.scalar(select(User).where(User.user_id == user_id))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

def find_user_by_name(user_name: str, db: db_dependency) -> User:
    result = db.scalar(select(User).where(User.name == user_name))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

def find_all_users(db: db_dependency) -> list[User]:
    result = db.scalars(select(User)).all()
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result

# get individual user by ID
@router.get("/user_id/{user_id}", response_model=schema.UserResponse)
async def read_user(user_id: int, db: db_dependency):
    return find_user_by_id(user_id, db)

# get individual user by Name
@router.get("/user_name/{user_name}", response_model=schema.UserResponse)
async def read_user_by_name(user_name: str, db: db_dependency):
    return find_user_by_name(user_name, db)

# get all users
@router.get("/", response_model=list[schema.UserResponse])
async def read_users(db: db_dependency):
    return find_all_users(db)

# create a new user
@router.post("/", response_model=schema.UserResponse)
async def create_user(user: schema.UserCreate, db: db_dependency):
    db_user = User(
        name=user.name,
        date_of_birth=user.date_of_birth,
        phone_number=user.phone_number,
        email=user.email,
        address=user.address
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# update an existing user
@router.patch("/{user_id}", response_model=schema.UserResponse)
async def update_user(user_id: int, user: schema.UserUpdate, db: db_dependency):
    db_user = find_user_by_id(user_id, db)
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# delete an existing user
@router.delete("/user_id/{user_id}", response_model=schema.UserResponse)
async def delete_user(user_id: int, db: db_dependency):
    db_user = find_user_by_id(user_id, db)
    db.delete(db_user)
    db.commit()
    return db_user

# delete an existing user by name
@router.delete("/user_name/{user_name}", response_model=schema.UserResponse)
async def delete_user_by_name(user_name: str, db: db_dependency):
    db_user = find_user_by_name(user_name, db)
    db.delete(db_user)
    db.commit()
    return db_user