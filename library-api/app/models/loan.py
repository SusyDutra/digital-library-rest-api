from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base

class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    fine_amount = Column(Float, default=0.0)
    status = Column(String(20), default="active")

    book = relationship("Book")
    user = relationship("User")