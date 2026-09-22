from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    BigInteger,
)
from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_created = Column(Date)
    description = Column(String)
    expenditure = Column(Boolean)

    __unique_constraints__ = UniqueConstraint("name", name="unique_name_created")


class Activity_logs(Base):
    __tablename__ = "activity_logs"

    activity_log_id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.activity_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    date_created = Column(Date)
    net_gain = Column(BigInteger)
