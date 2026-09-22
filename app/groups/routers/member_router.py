from fastapi import APIRouter, Request
from app.groups.models import Member
from app.groups import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/members", tags=["members"])

group_crud = CRUDBase[Member, schema.MemberCreate, schema.MemberUpdate](
    Member, not_found_detail="Member not found"
)


# search members
@router.get("/", response_model=list[schema.MemberResponse])
async def search_members(request: Request, db: db_dependency):
    filters = build_filters(Member, request.query_params)
    return group_crud.search(db, filters)


# create a new member
@router.post("/", response_model=schema.MemberResponse)
async def create_member(member: schema.MemberCreate, db: db_dependency):
    return group_crud.create(db, member)


# update the member matching the query filters, e.g. /members/?member_id=1
@router.patch("/", response_model=schema.MemberResponse)
async def update_member(
    request: Request, member: schema.MemberUpdate, db: db_dependency
):
    filters = group_crud.require_filters(build_filters(Member, request.query_params))
    db_member = group_crud.get_by(db, **filters)
    return group_crud.update(db, db_member, member)


# delete member(s) matching the query filters, e.g. /members/?member_id=2
@router.delete("/", response_model=list[schema.MemberResponse])
async def delete_members(request: Request, db: db_dependency):
    filters = group_crud.require_filters(build_filters(Member, request.query_params))
    db_members = group_crud.get_many_by(db, **filters)
    return group_crud.delete_many(db, db_members)


# delete all members
@router.delete("/all", response_model=list[schema.MemberResponse])
async def delete_all_members(db: db_dependency):
    return group_crud.delete_all(db)
