from sqlalchemy import select
from app.users.models import Account, User, Platform
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from fastapi import Request
from sqlalchemy.orm import joinedload

account_crud = CRUDBase[Account, schema.AccountCreate, schema.AccountUpdate](
    Account, not_found_detail="Account not found"
)



def search_accounts(
    db: db_dependency,
    user_name: str | None = None,
    platform_name: str | None = None,
    username: str | None = None,
    active_status: bool | None = None,
):
    statement = select(Account).options(
        joinedload(Account.user),
        joinedload(Account.platform),
    )

    if user_name is not None:
        statement = statement.where(
            Account.user.has(User.name.ilike(f"%{user_name}%"))
        )

    if platform_name is not None:
        statement = statement.where(
            Account.platform.has(Platform.name.ilike(f"%{platform_name}%"))
        )

    if username is not None:
        statement = statement.where(Account.username.ilike(f"%{username}%"))

    if active_status is not None:
        statement = statement.where(Account.active_status == active_status)

    return db.scalars(statement).all()