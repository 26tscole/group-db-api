from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from app.database import Base

class Bot(Base):
    __tablename__ = "bots"

    bot_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    model = Column(String, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    personality = Column(String, nullable=False)

class Bot_chat_logs(Base):
    __tablename__ = "bot_chats"

    bot_chat_log_id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.bot_id"), nullable=False)
    chat_location = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)