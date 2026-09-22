from datetime import date
from pydantic import BaseModel


class ActivityCreate(BaseModel):
    name: str
    date_created: date
    description: str
    expenditure: bool


class ActivityUpdate(BaseModel):
    date_created: date | None = None
    name: str | None = None
    description: str | None = None
    expenditure: bool | None = None


class ActivityResponse(ActivityCreate):
    activity_id: int

    model_config = {"from_attributes": True}


class ActivityLogCreate(BaseModel):
    activity_id: int
    group_id: int
    date_created: date
    net_gain: int


class ActivityLogUpdate(BaseModel):
    activity_id: int | None = None
    group_id: int | None = None
    date_created: date | None = None
    net_gain: int | None = None


class ActivityLogResponse(ActivityLogCreate):
    activity_log_id: int

    model_config = {"from_attributes": True}
