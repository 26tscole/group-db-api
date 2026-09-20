from datetime import date
from pydantic import BaseModel

class ActivityCreate(BaseModel):
    name: str
    date_of_birth: date
    phone_number: str
    email: str
    address: str

class ActivityUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None

class ActivityResponse(ActivityCreate):
    activity_id: int

    model_config = { "from_attributes": True }

class ActivityLogCreate(BaseModel):
    activity_id: int
    user_id: int
    timestamp: date

class ActivityLogUpdate(BaseModel):
    activity_id: int | None = None
    user_id: int | None = None
    timestamp: date | None = None

class ActivityLogResponse(ActivityLogCreate):
    activity_log_id: int

    model_config = { "from_attributes": True }