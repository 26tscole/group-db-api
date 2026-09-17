from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint, BigInteger
from app.database import Base

    
class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    expenditure = Column(BigInteger)

class Activity_logs(Base):
    __tablename__ = "activity_logs"

    activity_log_id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.activity_id"))
    group_id = Column(Integer,ForeignKey("groups.group_id"))
    date = Column(String)
    net_expenditure = Column(BigInteger)
