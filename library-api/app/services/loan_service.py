from repositories.loan_repository import LoanRepository
from schemas.loan import LoanCreate

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository

