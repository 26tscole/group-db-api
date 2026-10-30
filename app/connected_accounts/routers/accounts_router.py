from fastapi import APIRouter, Request
from app.users.models import Account
from app.users import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency
from app.connected_accounts.services.accounts_service import search_accounts

router = APIRouter(prefix="/accounts", tags=["accounts"])

