from fastapi import APIRouter, Request
from app.users.models import Account
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency
from app.users.services.accounts_service import search_accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=list[schema.AccountWithDetails])
def get_accounts(
    request: Request,
    user_name: str | None = None,
    platform_name: str | None = None,
    username: str | None = None,
    active_status: bool | None = None,
):
    db = request.state.db
    accounts = search_accounts(
        db=db,
        user_name=user_name,
        platform_name=platform_name,
        username=username,
        active_status=active_status,
    )
    return accounts