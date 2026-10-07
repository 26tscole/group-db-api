from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    address = Column(String)
    accounts = relationship("Account", back_populates="user")


    # only one user with the same email
    __table_args__ = (UniqueConstraint("email", name="unique_user"),)


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    platform_id = Column(Integer, ForeignKey("platforms.platform_id"))
    username = Column(String)
    active_status = Column(Boolean, nullable=False)
    user = relationship("User", back_populates="accounts")
    platform = relationship("Platform", back_populates="accounts")

    # Ensure that each user can only have one account per platform
    __table_args__ = (
        UniqueConstraint("platform_id", "username", name="unique_platform_account"),
    )


class Platform(Base):
    __tablename__ = "platforms"

    platform_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    accounts = relationship("Account", back_populates="platform")
