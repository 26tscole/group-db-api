from fastapi import APIRouter, Request
from app.users import schema
from app.dependencies import db_dependency
from app.users.services.platforms_service import (
    search_platforms,
    create_platform,
    update_platform,
    delete_platforms,
    delete_all_platforms,
)

router = APIRouter(prefix="/platforms", tags=["platforms"])

# search platforms
@router.get("/", response_model=list[schema.PlatformResponse])
async def search_platforms_endpoint(request: Request, db: db_dependency):
    return search_platforms(request, db)


# create a new platform
@router.post("/", response_model=schema.PlatformResponse)
async def create_platform_endpoint(platform: schema.PlatformCreate, db: db_dependency):
    return create_platform(platform, db)


# update the platform matching the query filters, e.g. /platforms/?platform_id=1
@router.patch("/", response_model=schema.PlatformResponse)
async def update_platform_endpoint(request: Request, platform: schema.PlatformUpdate, db: db_dependency):
    return update_platform(request, platform, db)


# delete platform(s) matching the query filters, e.g. /platforms/?platform_id=2
@router.delete("/", response_model=list[schema.PlatformResponse])
async def delete_platforms_endpoint(request: Request, db: db_dependency):
    return delete_platforms(request, db)


# delete all platforms
@router.delete("/all", response_model=list[schema.PlatformResponse])
async def delete_all_platforms_endpoint(db: db_dependency):
    return delete_all_platforms(db)