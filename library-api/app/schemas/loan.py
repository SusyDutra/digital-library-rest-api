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
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True