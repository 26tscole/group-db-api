
from pydantic import AliasChoices, BaseModel, Field
from datetime import date


class AccountCreate(BaseModel):
    user_id: int
    platform_id: int
    username: str
    external_id: str
    access_token: str
    refresh_token: str
    created_at: str
    active_status: bool


class AccountUpdate(BaseModel):
    user_id: int | None = None
    platform_id: int | None = None
    username: str | None = None
    active_status: bool | None = None


class AccountResponse(AccountCreate):
    id: int

    model_config = {"from_attributes": True}


class PlatformCreate(BaseModel):
    name: str
    url: str


class PlatformUpdate(BaseModel):
    name: str | None = None
    url: str | None = None


class PlatformResponse(PlatformCreate):
    id: int

    model_config = {"from_attributes": True}