from pydantic import BaseModel


class DebtCreate(BaseModel):
    activity_log_id: int
    creditor_id: int
    debtor_id: int
    reason: str
    satisified: bool
    amount: int


class DebtUpdate(BaseModel):
    activity_log_id: int | None = None
    creditor_id: int | None = None
    debtor_id: int | None = None
    reason: str | None = None
    satisified: bool | None = None
    amount: int | None = None


class DebtResponse(DebtCreate):
    debt_id: int

    model_config = {"from_attributes": True}
