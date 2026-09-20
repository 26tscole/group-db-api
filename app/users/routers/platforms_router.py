from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.users.models import Platform
from app.users import schema
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/platforms",
    tags=["platforms"]
)

def find_platform_by_id(platform_id: int, db: db_dependency) -> Platform:
    result = db.scalar(select(Platform).where(Platform.platform_id == platform_id))
    if not result:
        raise HTTPException(status_code=404, detail="Platform not found")
    return result

def find_platform_by_name(platform_name: str, db: db_dependency) -> Platform:
    result = db.scalar(select(Platform).where(Platform.name == platform_name))
    if not result:
        raise HTTPException(status_code=404, detail="Platform not found")
    return result

def find_all_platforms(db: db_dependency) -> list[Platform]:
    result = db.scalars(select(Platform)).all()
    if not result:
        raise HTTPException(status_code=404, detail="No platforms found")
    return result

# get individual platform by ID
@router.get("/platform_id/{platform_id}", response_model=schema.PlatformResponse)
async def read_platform(platform_id: int, db: db_dependency):
    return find_platform_by_id(platform_id, db)

# get individual platform by Name
@router.get("/platform_name/{platform_name}", response_model=schema.PlatformResponse)
async def read_platform_by_name(platform_name: str, db: db_dependency):
    return find_platform_by_name(platform_name, db)

# get all platforms
@router.get("/", response_model=list[schema.PlatformResponse])
async def read_platforms(db: db_dependency):
    return find_all_platforms(db)

# create a new platform
@router.post("/", response_model=schema.PlatformResponse)
async def create_platform(platform: schema.PlatformCreate, db: db_dependency):
    db_platform = Platform(
        name=platform.name,
        url=platform.url
    )
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    return db_platform

# update an existing platform
@router.patch("/{platform_id}", response_model=schema.PlatformResponse)
async def update_platform(platform_id: int, platform: schema.PlatformUpdate, db: db_dependency):
    db_platform = find_platform_by_id(platform_id, db)
    for field, value in platform.model_dump(exclude_unset=True).items():
        setattr(db_platform, field, value)
    db.commit()
    db.refresh(db_platform)
    return db_platform

# delete an existing platform
@router.delete("/platform_id/{platform_id}", response_model=schema.PlatformResponse)
async def delete_platform(platform_id: int, db: db_dependency):
    db_platform = find_platform_by_id(platform_id, db)
    db.delete(db_platform)
    db.commit()
    return db_platform

# delete an existing platform by name
@router.delete("/platform_name/{platform_name}", response_model=schema.PlatformResponse)
async def delete_platform_by_name(platform_name: str, db: db_dependency):
    db_platform = find_platform_by_name(platform_name, db)
    db.delete(db_platform)
    db.commit()
    return db_platform