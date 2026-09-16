from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str
    owner: int
    date_created: str
    parent_group_id: int | None = None

class GroupUpdate(BaseModel):
    name: str | None = None
    owner: int | None = None
    date_created: str | None = None
    parent_group_id: int | None = None

class GroupResponse(GroupCreate):
    group_id: int

    model_config = { "from_attributes": True }

class MemberCreate(BaseModel):
    group_id: int
    user_id: int
    date_joined: str

class MemberResponse(MemberCreate):
    member_id: int

    model_config = { "from_attributes": True }