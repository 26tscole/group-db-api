from fastapi import APIRouter, Request
from app.connected_accounts.models import Account
from app.connected_accounts import schema
from app.crud import CRUDBase, build_filters
from app.db_deps import db_dependency

router = APIRouter(prefix="/accounts", tags=["accounts"])

