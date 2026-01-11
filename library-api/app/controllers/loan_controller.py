from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import SessionLocal
from services.loan_service import LoanService
from repositories.loan_repository import LoanRepository
from schemas.loan import Loan, LoanCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
