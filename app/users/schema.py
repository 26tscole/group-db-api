from datetime import date
from pydantic import AliasChoices, BaseModel, Field


class createUserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: str
    email: str
    address: str

class TokenData(BaseModel):
    access_token: str
    token_type: str

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


class UserResponse(BaseModel):
    id: int 
    username: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: str | None = None
    email: str
    address: str | None = None

    model_config = {"from_attributes": True}


class AccountCreate(BaseModel):
    user_id: int
    platform_id: int
    username: str
    active_status: bool


class AccountUpdate(BaseModel):
    user_id: int | None = None
    platform_id: int | None = None
    username: str | None = None
    active_status: bool | None = None


class AccountResponse(AccountCreate):
    account_id: int

    model_config = {"from_attributes": True}


class PlatformCreate(BaseModel):
    name: str
    url: str


class PlatformUpdate(BaseModel):
    name: str | None = None
    url: str | None = None


class PlatformResponse(PlatformCreate):
    platform_id: int
    url: str | None = None

    model_config = {"from_attributes": True}


class UserSummary(BaseModel):
    user_id: int
    name: str
    model_config = {"from_attributes": True}


class PlatformSummary(BaseModel):
    platform_id: int
    name: str | None
    url: str | None
    model_config = {"from_attributes": True}


class AccountWithDetails(AccountResponse):
    user: UserSummary | None = None
    platform: PlatformSummary | None = None