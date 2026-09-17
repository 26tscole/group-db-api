from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from app.groups.models import Member, Group
from app.groups import schema
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
)


def find_group_by_id(group_id: int, db: db_dependency) -> Group:
    result = db.scalar(select(Group).where(Group.group_id == group_id))
    if not result:
        raise HTTPException(status_code=404, detail="Group not found")
    return result

def find_group_by_name(group_name: str, db: db_dependency) -> Group:
    result = db.scalar(select(Group).where(Group.name == group_name))
    if not result:
        raise HTTPException(status_code=404, detail="Group not found")
    return result

def find_all_groups(db: db_dependency) -> list[Group]:
    result = db.scalars(select(Group)).all()
    if not result:
        raise HTTPException(status_code=404, detail="No groups found")
    return result

# get individual group by ID
@router.get("/id/{group_id}", response_model=schema.GroupResponse)
async def read_group(group_id: int, db: db_dependency):
    return find_group_by_id(group_id, db)

# get individual group by Name
@router.get("/name/{group_name}", response_model=schema.GroupResponse)
async def read_group_by_name(group_name: str, db: db_dependency):
    return find_group_by_name(group_name, db)

# get all groups
@router.get("/", response_model=list[schema.GroupResponse])
async def read_groups(db: db_dependency):
    return find_all_groups(db)

# create a new group
@router.post("/", response_model=schema.GroupResponse)
async def create_group(group: schema.GroupCreate, db: db_dependency):
    db_group = Group(
        name=group.name,
        owner=group.owner,
        date_created=group.date_created,
        parent_group_id=group.parent_group_id
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# update an existing group
@router.patch("/{group_id}", response_model=schema.GroupResponse)
async def update_group(group_id: int, group: schema.GroupUpdate, db: db_dependency):
    db_group = find_group_by_id(group_id, db)
    for field, value in group.model_dump(exclude_unset=True).items():
        setattr(db_group, field, value)
    db.commit()
    db.refresh(db_group)
    return db_group

# delete an existing group
@router.delete("/{group_id}", response_model=schema.GroupResponse)
async def delete_group(group_id: int, db: db_dependency):
    db_group = find_group_by_id(group_id, db)
    db.delete(db_group)
    db.commit()
    return db_group