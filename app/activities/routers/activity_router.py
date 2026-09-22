from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.activities.models import Activity
from app.activities import schema
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)

def find_activity_by_id(activity_id: int, db: db_dependency) -> Activity:
    result = db.scalar(select(Activity).where(Activity.activity_id == activity_id))
    if not result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result

def find_activity_by_name(name: str, db: db_dependency) -> Activity:
    result = db.scalar(select(Activity).where(Activity.name == name))
    if not result:
        raise HTTPException(status_code=404, detail="Activity not found")
    return result

def find_all_activities(db: db_dependency) -> list[Activity]:
    result = db.scalars(select(Activity)).all()
    if not result:
        raise HTTPException(status_code=404, detail="No activities found")
    return result

# get individual activity by ID
@router.get("/activity_id/{activity_id}", response_model=schema.ActivityResponse)
async def read_activity(activity_id: int, db: db_dependency):
    return find_activity_by_id(activity_id, db)

# get individual activity by Name
@router.get("/name/{name}", response_model=schema.ActivityResponse)
async def read_activity_by_name(name: str, db: db_dependency):
    return find_activity_by_name(name, db)

# get all activities
@router.get("/", response_model=list[schema.ActivityResponse])
async def read_activities(db: db_dependency):
    return find_all_activities(db)

# create a new activity
@router.post("/", response_model=schema.ActivityResponse)
async def create_activity(activity: schema.ActivityCreate, db: db_dependency):
    db_activity = Activity(
        name=activity.name,
        date_created=activity.date_created,
        description=activity.description,
        expenditure=activity.expenditure
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# update an existing activity
@router.patch("/activity_id/{activity_id}", response_model=schema.ActivityResponse)
async def update_activity(activity_id: int, activity: schema.ActivityUpdate, db: db_dependency):
    db_activity = find_activity_by_id(activity_id, db)
    for field, value in activity.model_dump(exclude_unset=True).items():
        setattr(db_activity, field, value)
    db.commit()
    db.refresh(db_activity)
    return db_activity

# delete an existing activity by ID
@router.delete("/activity_id/{activity_id}", response_model=schema.ActivityResponse)
async def delete_activity(activity_id: int, db: db_dependency):
    db_activity = find_activity_by_id(activity_id, db)
    db.delete(db_activity)
    db.commit()
    return db_activity

# delete an existing activity by Name
@router.delete("/name/{name}", response_model=schema.ActivityResponse)
async def delete_activity_by_name(name: str, db: db_dependency):
    db_activity = find_activity_by_name(name, db)
    db.delete(db_activity)
    db.commit()
    return db_activity