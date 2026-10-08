from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String)
    email = Column(String, nullable=False, unique=True)
    address = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    accounts = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    username = Column(String, nullable=False)
    external_id = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    active_status = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="accounts")
    platform = relationship("Platform", back_populates="accounts")

    __table_args__ = (
        UniqueConstraint("platform_id", "username", name="uq_accounts_platform_username"),
        UniqueConstraint("platform_id", "external_id", name="uq_accounts_platform_external_id"),
    )


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    accounts = relationship(
        "Account", back_populates="platform", cascade="all, delete-orphan"
    )
