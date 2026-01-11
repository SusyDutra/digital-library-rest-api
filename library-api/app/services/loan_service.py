from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate
from datetime import datetime, timedelta
from fastapi import HTTPException

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository
    def get_user_loans(self, user_id: int):
        return self.repository.get_user_loans(user_id)
