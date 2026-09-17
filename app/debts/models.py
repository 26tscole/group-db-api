from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from app.database import Base

class Debt(Base):
    __tablename__ = "debts"

    debt_id = Column(Integer, primary_key=True, index=True)
    creditor_id = Column(Integer, ForeignKey("users.user_id"))
    debtor_id = Column(Integer, ForeignKey("users.user_id"))
    reason = Column(String)
    satisified = Column(Boolean)
    amount = Column(BigInteger)
