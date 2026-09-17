from datetime import date
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    date_of_birth: date
    phone_number: str
    email: str
    address: str

class UserUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    phone_number: str | None = None
    email: str | None = None
    address: str | None = None

class UserResponse(UserCreate):
    user_id: int

    model_config = { "from_attributes": True }

class AccountCreate(BaseModel):
    platform_id: int
    username: str
    active_status: bool

class AccountUpdate(BaseModel):
    platform_id: int | None = None
    username: str | None = None
    active_status: bool | None = None

class AccountResponse(AccountCreate):
    account_id: int

    model_config = { "from_attributes": True }

class PlatformCreate(BaseModel):
    name: str
    website: str

class PlatformUpdate(BaseModel):
    name: str | None = None
    website: str | None = None

class PlatformResponse(PlatformCreate):
    platform_id: int

    model_config = { "from_attributes": True }