from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from app.database import Base


class Debt(Base):
    __tablename__ = "debts"

    debt_id = Column(Integer, primary_key=True, index=True)
    activity_log_id = Column(Integer, ForeignKey("activity_logs.activity_log_id"))
    creditor_id = Column(Integer, ForeignKey("members.member_id"))
    debtor_id = Column(Integer, ForeignKey("members.member_id"))
    reason = Column(String)
    satisfied = Column(Boolean)
    amount = Column(BigInteger)
