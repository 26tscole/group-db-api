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


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
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
