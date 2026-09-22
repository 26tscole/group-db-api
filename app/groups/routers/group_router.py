from fastapi import APIRouter, Request
from app.groups.models import Group
from app.groups import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/groups", tags=["groups"])

group_crud = CRUDBase[Group, schema.GroupCreate, schema.GroupUpdate](
    Group, not_found_detail="Group not found"
)


# search groups
@router.get("/", response_model=list[schema.GroupResponse])
async def search_groups(request: Request, db: db_dependency):
    filters = build_filters(Group, request.query_params)
    return group_crud.search(db, filters)


# create a new group
@router.post("/", response_model=schema.GroupResponse)
async def create_group(group: schema.GroupCreate, db: db_dependency):
    return group_crud.create(db, group)


# update the group matching the query filters, e.g. /groups/?group_id=1
@router.patch("/", response_model=schema.GroupResponse)
async def update_group(request: Request, group: schema.GroupUpdate, db: db_dependency):
    filters = group_crud.require_filters(build_filters(Group, request.query_params))
    db_group = group_crud.get_by(db, **filters)
    return group_crud.update(db, db_group, group)


# delete group(s) matching the query filters, e.g. /groups/?group_id=2
@router.delete("/", response_model=list[schema.GroupResponse])
async def delete_groups(request: Request, db: db_dependency):
    filters = group_crud.require_filters(build_filters(Group, request.query_params))
    db_groups = group_crud.get_many_by(db, **filters)
    return group_crud.delete_many(db, db_groups)


# delete all groups
@router.delete("/all", response_model=list[schema.GroupResponse])
async def delete_all_groups(db: db_dependency):
    return group_crud.delete_all(db)
