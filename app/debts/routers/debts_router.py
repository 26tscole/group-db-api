from fastapi import APIRouter, Request
from app.debts.models import Debt
from app.debts import schema
from app.crud import CRUDBase, build_filters
from app.dependencies import db_dependency

router = APIRouter(
    prefix="/debts",
    tags=["debts"]
)

debt_crud = CRUDBase[Debt, schema.DebtCreate, schema.DebtUpdate](Debt, not_found_detail="Debt not found")

# search debts, e.g. /debts/?creditor_id=3 or /debts/?debt_id=1&debtor_id=2
@router.get("/", response_model=list[schema.DebtResponse])
async def search_debts(request: Request, db: db_dependency):
    filters = build_filters(Debt, request.query_params)
    return debt_crud.search(db, filters)

# create a new debt
@router.post("/", response_model=schema.DebtResponse)
async def create_debt(debt: schema.DebtCreate, db: db_dependency):
    return debt_crud.create(db, debt)

# update the debt matching the query filters, e.g. /debts/?debt_id=1
@router.patch("/", response_model=schema.DebtResponse)
async def update_debt(request: Request, debt: schema.DebtUpdate, db: db_dependency):
    filters = debt_crud.require_filters(build_filters(Debt, request.query_params))
    db_debt = debt_crud.get_by(db, **filters)
    return debt_crud.update(db, db_debt, debt)

# delete debt(s) matching the query filters, e.g. /debts/?debtor_id=2
@router.delete("/", response_model=list[schema.DebtResponse])
async def delete_debts(request: Request, db: db_dependency):
    filters = debt_crud.require_filters(build_filters(Debt, request.query_params))
    db_debts = debt_crud.get_many_by(db, **filters)
    return debt_crud.delete_many(db, db_debts)

# delete all debts
@router.delete("/all", response_model=list[schema.DebtResponse])
async def delete_all_debts(db: db_dependency):
    return debt_crud.delete_all(db)