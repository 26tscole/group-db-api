from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, UniqueConstraint
from app.database import Base

    
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    address = Column(String)

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    platform_id = Column(Integer, ForeignKey("platforms.platform_id"))
    username = Column(String)
    active_status = Column(Boolean, nullable=False)

    # Ensure that each user can only have one account per platform
    __table_args__ = (
        UniqueConstraint("platform_id", "username", name="unique_platform_account"),
    )

class Platform(Base):
    __tablename__ = "platforms"

    platform_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    website = Column(String)