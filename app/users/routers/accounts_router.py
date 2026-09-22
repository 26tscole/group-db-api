from fastapi import APIRouter, Request
from app.users.models import Account
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(prefix="/accounts", tags=["accounts"])

account_crud = CRUDBase[Account, schema.AccountCreate, schema.AccountUpdate](
    Account, not_found_detail="Account not found"
)


# search accounts
@router.get("/", response_model=list[schema.AccountResponse])
async def search_accounts(request: Request, db: db_dependency):
    filters = build_filters(Account, request.query_params)
    return account_crud.search(db, filters)


# create a new account
@router.post("/", response_model=schema.AccountResponse)
async def create_account(account: schema.AccountCreate, db: db_dependency):
    return account_crud.create(db, account)


# update the account matching the query filters, e.g. /accounts/?account_id=1
@router.patch("/", response_model=schema.AccountResponse)
async def update_account(
    request: Request, account: schema.AccountUpdate, db: db_dependency
):
    filters = account_crud.require_filters(build_filters(Account, request.query_params))
    db_account = account_crud.get_by(db, **filters)
    return account_crud.update(db, db_account, account)


# delete account(s) matching the query filters, e.g. /accounts/?account_id=2
@router.delete("/", response_model=list[schema.AccountResponse])
async def delete_accounts(request: Request, db: db_dependency):
    filters = account_crud.require_filters(build_filters(Account, request.query_params))
    db_accounts = account_crud.get_many_by(db, **filters)
    return account_crud.delete_many(db, db_accounts)


# delete all accounts
@router.delete("/all", response_model=list[schema.AccountResponse])
async def delete_all_accounts(db: db_dependency):
    return account_crud.delete_all(db)
