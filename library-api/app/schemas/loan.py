from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanBase(BaseModel):
    book_id: int
    user_id: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    fine_amount: float = 0.0
    status: str = "active"

    class Config:
        from_attributes = True

class LoanReturn(BaseModel):
    fine_amount: float
    message: str