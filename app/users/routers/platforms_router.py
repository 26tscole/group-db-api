from fastapi import APIRouter, Request
from app.users.models import Platform
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/platforms", tags=["platforms"])

platform_crud = CRUDBase[Platform, schema.PlatformCreate, schema.PlatformUpdate](
    Platform, not_found_detail="Platform not found"
)


# search groups
@router.get("/", response_model=list[schema.PlatformResponse])
async def search_platforms(request: Request, db: db_dependency):
    filters = build_filters(Platform, request.query_params)
    return platform_crud.search(db, filters)


# create a new group
@router.post("/", response_model=schema.PlatformResponse)
async def create_platform(platform: schema.PlatformCreate, db: db_dependency):
    return platform_crud.create(db, platform)


# update the platform matching the query filters, e.g. /platforms/?platform_id=1
@router.patch("/", response_model=schema.PlatformResponse)
async def update_platform(
    request: Request, platform: schema.PlatformUpdate, db: db_dependency
):
    filters = platform_crud.require_filters(
        build_filters(Platform, request.query_params)
    )
    db_platform = platform_crud.get_by(db, **filters)
    return platform_crud.update(db, db_platform, platform)


# delete platform(s) matching the query filters, e.g. /platforms/?platform_id=2
@router.delete("/", response_model=list[schema.PlatformResponse])
async def delete_platforms(request: Request, db: db_dependency):
    filters = platform_crud.require_filters(
        build_filters(Platform, request.query_params)
    )
    db_platforms = platform_crud.get_many_by(db, **filters)
    return platform_crud.delete_many(db, db_platforms)


# delete all platforms
@router.delete("/all", response_model=list[schema.PlatformResponse])
async def delete_all_platforms(db: db_dependency):
    return platform_crud.delete_all(db)
