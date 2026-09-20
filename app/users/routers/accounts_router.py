from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from app.users.models import Account
from app.users import schema
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/platforms",
    tags=["platforms"]
)

def find_account_by_id(account_id: int, db: db_dependency) -> Account:
    result = db.scalar(select(Account).where(Account.account_id == account_id))
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

def find_account_by_username(username: str, db: db_dependency) -> Account:
    result = db.scalar(select(Account).where(Account.username == username))
    if not result:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

def find_all_accounts(db: db_dependency) -> list[Account]:
    result = db.scalars(select(Account)).all()
    if not result:
        raise HTTPException(status_code=404, detail="No accounts found")
    return result

# get individual account by ID
@router.get("/account_id/{account_id}", response_model=schema.AccountResponse)
async def read_account(account_id: int, db: db_dependency):
    return find_account_by_id(account_id, db)

# get individual account by Username
@router.get("/username/{username}", response_model=schema.AccountResponse)
async def read_account_by_username(username: str, db: db_dependency):
    return find_account_by_username(username, db)

# get all accounts
@router.get("/", response_model=list[schema.AccountResponse])
async def read_accounts(db: db_dependency):
    return find_all_accounts(db)

# create a new account
@router.post("/", response_model=schema.AccountResponse)
async def create_account(account: schema.AccountCreate, db: db_dependency):
    db_account = Account(
        user_id=account.user_id,
        platform_id=account.platform_id,
        username=account.username,
        active_status=account.active_status
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# update an existing account
@router.patch("/{account_id}", response_model=schema.AccountResponse)
async def update_account(account_id: int, account: schema.AccountUpdate, db: db_dependency):
    db_account = find_account_by_id(account_id, db)
    for field, value in account.model_dump(exclude_unset=True).items():
        setattr(db_account, field, value)
    db.commit()
    db.refresh(db_account)
    return db_account

# delete an existing account
@router.delete("/account_id/{account_id}", response_model=schema.AccountResponse)
async def delete_account(account_id: int, db: db_dependency):
    db_account = find_account_by_id(account_id, db)
    db.delete(db_account)
    db.commit()
    return db_account

# delete an existing account by username
@router.delete("/username/{username}", response_model=schema.AccountResponse)
async def delete_account_by_username(username: str, db: db_dependency):
    db_account = find_account_by_username(username, db)
    db.delete(db_account)
    db.commit()
    return db_account