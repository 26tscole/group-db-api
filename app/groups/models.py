from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from app.database import Base

    
class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner = Column(Integer, ForeignKey("users.user_id"))
    date_created = Column(String)
    parent_group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=True)

class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    user_id = Column(Integer,ForeignKey("users.user_id"))
    date_joined = Column(String)

    # Ensure that each user can only be a member of a group once
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="unique_group_member"),
    )

