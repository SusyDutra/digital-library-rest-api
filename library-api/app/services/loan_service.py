from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate
from app.logging_config import get_logger
from datetime import datetime, timedelta
from fastapi import HTTPException

logger = get_logger(__name__)

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository
        self.daily_fine = 2.0

    def get_all_loans(self, skip: int = 0, limit: int = 10):
        logger.debug("Fetching all loans from repository", skip=skip, limit=limit)
        return self.repository.get_all(skip, limit)

    def get_loans_count(self):
        count = self.repository.get_total_count()
        logger.debug("Retrieved loans count", total_count=count)
        return count

    def get_loan(self, loan_id: int):
        logger.debug("Fetching loan by ID", loan_id=loan_id)
        return self.repository.get_by_id(loan_id)

    def create_loan(self, loan: LoanCreate):
        logger.info("Creating loan", user_id=loan.user_id, book_id=loan.book_id)
        
        if not self.repository.check_book_availability(loan.book_id):
            logger.warning("Book not available for loan", book_id=loan.book_id)
            raise HTTPException(status_code=400, detail="Book is not available")
        
        user_active_loans = self.repository.get_user_active_loans(loan.user_id)
        if len(user_active_loans) >= 3:
            logger.warning("User has maximum active loans", user_id=loan.user_id, active_loans_count=len(user_active_loans))
            raise HTTPException(status_code=400, detail="User already has 3 active loans")
        
        created_loan = self.repository.create(loan)
        logger.info("Loan created successfully", loan_id=created_loan.id, user_id=loan.user_id, book_id=loan.book_id)
        return created_loan

    def return_book(self, loan_id: int):
        logger.info("Processing book return", loan_id=loan_id)
        
        loan = self.repository.get_by_id(loan_id)
        if not loan or loan.status != "active":
            logger.warning("Active loan not found for return", loan_id=loan_id)
            raise HTTPException(status_code=404, detail="Active loan not found")
        
        fine_amount = self._calculate_fine(loan.due_date)
        logger.info("Fine calculated", loan_id=loan_id, fine_amount=fine_amount, due_date=loan.due_date.isoformat())
        
        returned_loan = self.repository.return_book(loan_id, fine_amount)
        logger.info("Book returned successfully", loan_id=loan_id, fine_amount=fine_amount)
        return returned_loan

    def get_active_loans(self, skip: int = 0, limit: int = 10):
        logger.debug("Fetching active loans", skip=skip, limit=limit)
        return self.repository.get_active_loans(skip, limit)

    def get_active_loans_count(self):
        count = self.repository.get_active_loans_count()
        logger.debug("Retrieved active loans count", active_count=count)
        return count

    def get_overdue_loans(self, skip: int = 0, limit: int = 10):
        logger.debug("Fetching overdue loans", skip=skip, limit=limit)
        return self.repository.get_overdue_loans(skip, limit)

    def get_overdue_loans_count(self):
        count = self.repository.get_overdue_loans_count()
        logger.debug("Retrieved overdue loans count", overdue_count=count)
        return count

    def get_user_loans(self, user_id: int, skip: int = 0, limit: int = 10):
        logger.debug("Fetching user loans", user_id=user_id, skip=skip, limit=limit)
        return self.repository.get_user_loans(user_id, skip, limit)

    def get_user_loans_count(self, user_id: int):
        count = self.repository.get_user_loans_count(user_id)
        logger.debug("Retrieved user loans count", user_id=user_id, user_loans_count=count)
        return count

    def _calculate_fine(self, due_date: datetime) -> float:
        if datetime.utcnow() <= due_date:
            return 0.0
        
        days_overdue = (datetime.utcnow() - due_date).days
        fine = days_overdue * self.daily_fine
        logger.debug("Fine calculation", days_overdue=days_overdue, daily_fine=self.daily_fine, total_fine=fine)
        return fine