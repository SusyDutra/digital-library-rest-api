from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.schemas.loan import LoanCreate
from datetime import datetime, timedelta

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_loans(self):
        return self.db.query(Loan).filter(Loan.status == "active").all()

    def get_overdue_loans(self):
        return self.db.query(Loan).filter(
            Loan.status == "active",
            Loan.due_date < datetime.utcnow()
        ).all()

    def get_user_loans(self, user_id: int):
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()
