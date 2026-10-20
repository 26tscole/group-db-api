from pydantic import BaseModel
from datetime import datetime


class BotCreate(BaseModel):
    group_id: int
    name: str
    model: str
    personality: str 


class BotUpdate(BaseModel):
    group_id: int | None = None
    name: str | None = None
    model: str | None = None
    personality: str | None = None


class BotResponse(BotCreate):
    bot_id: int

    model_config = {"from_attributes": True}


class BotChatLogsCreate(BaseModel):
    bot_id: int
    chat_location: str
    summary: str
    user_id: int | None = None
    start_time: datetime
    end_time: datetime


class BotChatLogsUpdate(BaseModel):
    bot_id: int | None = None
    chat_location: str | None = None
    summary: str | None = None
    user_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class BotChatLogsResponse(BotChatLogsCreate):
    chat_log_id: int

    model_config = {"from_attributes": True}
