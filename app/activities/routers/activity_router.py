from fastapi import APIRouter, Request
from app.activities.models import Activity
from app.activities import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/activities", tags=["activities"])

activity_crud = CRUDBase[Activity, schema.ActivityCreate, schema.ActivityUpdate](
    Activity, not_found_detail="Activity not found"
)


# search activities, e.g. /activities/?activity_id=5 or /activities/?activity_id=1
@router.get("/", response_model=list[schema.ActivityResponse])
async def search_activities(request: Request, db: db_dependency):
    filters = build_filters(Activity, request.query_params)
    return activity_crud.search(db, filters)


# create a new activity
@router.post("/", response_model=schema.ActivityResponse)
async def create_activity(activity: schema.ActivityCreate, db: db_dependency):
    return activity_crud.create(db, activity)


# update activity(s) matching the query filters, e.g. /activities/?activity_id=1
@router.patch("/", response_model=schema.ActivityResponse)
async def update_activity(
    request: Request, activity: schema.ActivityUpdate, db: db_dependency
):
    filters = activity_crud.require_filters(
        build_filters(Activity, request.query_params)
    )
    db_activity = activity_crud.get_by(db, **filters)
    return activity_crud.update(db, db_activity, activity)


# delete activity(s) matching the query filters, e.g. /activities/?activity_id=5
@router.delete("/", response_model=list[schema.ActivityResponse])
async def delete_activities(request: Request, db: db_dependency):
    filters = activity_crud.require_filters(
        build_filters(Activity, request.query_params)
    )
    db_activities = activity_crud.get_many_by(db, **filters)
    return activity_crud.delete_many(db, db_activities)


# delete all activities
@router.delete("/all", response_model=list[schema.ActivityResponse])
async def delete_all_activities(db: db_dependency):
    return activity_crud.delete_all(db)
