from sqlalchemy import select
from app.connected_accounts.models import Account, Platform
from app.connected_accounts import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from fastapi import Request
from sqlalchemy.orm import joinedload

account_crud = CRUDBase[Account, schema.AccountCreate, schema.AccountUpdate](
    Account, not_found_detail="Account not found"
)


