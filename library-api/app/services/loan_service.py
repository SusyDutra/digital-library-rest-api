from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate
from datetime import datetime, timedelta
from fastapi import HTTPException

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository
        self.daily_fine = 2.0

    def get_all_loans(self):
        return self.repository.get_all()
    def create_loan(self, loan: LoanCreate):
        if not self.repository.check_book_availability(loan.book_id):
            raise HTTPException(status_code=400, detail="Book is not available")
        
        user_active_loans = self.repository.get_user_active_loans(loan.user_id)
        if len(user_active_loans) >= 3:
            raise HTTPException(status_code=400, detail="User already has 3 active loans")
        
        return self.repository.create(loan)

    def return_book(self, loan_id: int):
        loan = self.repository.get_by_id(loan_id)
        if not loan or loan.status != "active":
            raise HTTPException(status_code=404, detail="Active loan not found")
        
        fine_amount = self._calculate_fine(loan.due_date)
        return self.repository.return_book(loan_id, fine_amount)

    def get_active_loans(self):
        return self.repository.get_active_loans()

    def get_overdue_loans(self):
        return self.repository.get_overdue_loans()

    def get_user_loans(self, user_id: int):
        return self.repository.get_user_loans(user_id)

    def _calculate_fine(self, due_date: datetime) -> float:
        if datetime.utcnow() <= due_date:
            return 0.0
        
        days_overdue = (datetime.utcnow() - due_date).days
        return days_overdue * self.daily_fine