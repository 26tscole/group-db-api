from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Members(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    discord = Column(String, index=True)
    birthdate = Column(String, index=True)

