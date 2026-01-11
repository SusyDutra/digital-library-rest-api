from sqlalchemy.orm import Session
from models.loan import Loan
from schemas.loan import LoanCreate
from datetime import datetime

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

