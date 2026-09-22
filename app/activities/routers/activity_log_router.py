from fastapi import APIRouter, Request
from app.activities.models import Activity_logs
from app.activities import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/activity_logs", tags=["activity_logs"])

activity_log_crud = CRUDBase[
    Activity_logs, schema.ActivityLogCreate, schema.ActivityLogUpdate
](Activity_logs, not_found_detail="Activity log not found")


# search activity logs, e.g. /activity_logs/?activity_id=5 or /activity_logs/?activity_log_id=1
@router.get("/", response_model=list[schema.ActivityLogResponse])
async def search_activity_logs(request: Request, db: db_dependency):
    filters = build_filters(Activity_logs, request.query_params)
    return activity_log_crud.search(db, filters)


# create a new activity log
@router.post("/", response_model=schema.ActivityLogResponse)
async def create_activity_log(
    activity_log: schema.ActivityLogCreate, db: db_dependency
):
    return activity_log_crud.create(db, activity_log)


# update activity log(s) matching the query filters, e.g. /activity_logs/?activity_log_id=1
@router.patch("/", response_model=schema.ActivityLogResponse)
async def update_activity_log(
    request: Request, activity_log: schema.ActivityLogUpdate, db: db_dependency
):
    filters = activity_log_crud.require_filters(
        build_filters(Activity_logs, request.query_params)
    )
    db_activity_log = activity_log_crud.get_by(db, **filters)
    return activity_log_crud.update(db, db_activity_log, activity_log)


# delete activity log(s) matching the query filters, e.g. /activity_logs/?activity_id=5
@router.delete("/", response_model=list[schema.ActivityLogResponse])
async def delete_activity_logs(request: Request, db: db_dependency):
    filters = activity_log_crud.require_filters(
        build_filters(Activity_logs, request.query_params)
    )
    db_activity_logs = activity_log_crud.get_many_by(db, **filters)
    return activity_log_crud.delete_many(db, db_activity_logs)


# delete all activity logs
@router.delete("/all", response_model=list[schema.ActivityLogResponse])
async def delete_all_activity_logs(db: db_dependency):
    return activity_log_crud.delete_all(db)
