from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.schemas.loan import LoanCreate
from datetime import datetime, timedelta

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Loan).all()

    def get_by_id(self, loan_id: int):
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def create(self, loan: LoanCreate):
        # Calculate due date as 14 days from now
        due_date = datetime.utcnow() + timedelta(days=14)
        
        loan_data = loan.dict()
        loan_data['due_date'] = due_date
        
        db_loan = Loan(**loan_data)
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def return_book(self, loan_id: int, fine_amount: float = 0.0):
        loan = self.get_by_id(loan_id)
        if loan and loan.status == "active":
            loan.return_date = datetime.utcnow()
            loan.fine_amount = fine_amount
            loan.status = "returned"
            self.db.commit()
        return loan

    def get_active_loans(self):
        return self.db.query(Loan).filter(Loan.status == "active").all()

    def get_overdue_loans(self):
        current_time = datetime.utcnow()
        return self.db.query(Loan).filter(
            Loan.status == "active",
            Loan.loan_date + timedelta(days=14) < current_time
        ).all()

    def get_user_loans(self, user_id: int):
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()

    def get_user_active_loans(self, user_id: int):
        return self.db.query(Loan).filter(
            Loan.user_id == user_id,
            Loan.status == "active"
        ).all()

    def check_book_availability(self, book_id: int):
        active_loan = self.db.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.status == "active"
        ).first()
        return active_loan is None