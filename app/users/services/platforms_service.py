from app.users.models import Platform
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency
from fastapi import Request

platform_crud = CRUDBase[Platform, schema.PlatformCreate, schema.PlatformUpdate](
    Platform, not_found_detail="Platform not found"
)

def search_platforms(request: Request, db: db_dependency):
    filters = build_filters(Platform, request.query_params)
    return platform_crud.search(db, filters)

def create_platform(platform: schema.PlatformCreate, db: db_dependency):
    return platform_crud.create(db, platform)

def update_platform(
    request: Request, platform: schema.PlatformUpdate, db: db_dependency
):
    filters = platform_crud.require_filters(
        build_filters(Platform, request.query_params)
    )
    db_platform = platform_crud.get_by(db, **filters)
    return platform_crud.update(db, db_platform, platform)

def delete_platforms(request: Request, db: db_dependency):
    filters = platform_crud.require_filters(
        build_filters(Platform, request.query_params)
    )
    db_platforms = platform_crud.get_many_by(db, **filters)
    return platform_crud.delete_many(db, db_platforms)

def delete_all_platforms(db: db_dependency):
    return platform_crud.delete_all(db)
