from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import Loan, LoanCreate, LoanReturn
from app.schemas.pagination import PaginatedResponse
import math

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/loans", response_model=PaginatedResponse[Loan])
def get_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar empréstimos"""
    skip = (page - 1) * size
    service = LoanService(LoanRepository(db))
    loans = service.get_all_loans(skip, size)
    total = service.get_loans_count()
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.post("/loans", response_model=Loan)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    """Realizar empréstimo de livro"""
    service = LoanService(LoanRepository(db))
    return service.create_loan(loan)

@router.put("/loans/{loan_id}/return", response_model=LoanReturn)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """Processar devolução com cálculo de multa"""
    service = LoanService(LoanRepository(db))
    loan = service.return_book(loan_id)
    return LoanReturn(
        fine_amount=loan.fine_amount,
        message=f"Book returned. Fine: R$ {loan.fine_amount:.2f}"
    )

@router.get("/loans/active", response_model=PaginatedResponse[Loan])
def get_active_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar empréstimos ativos"""
    skip = (page - 1) * size
    service = LoanService(LoanRepository(db))
    loans = service.get_active_loans(skip, size)
    total = service.get_active_loans_count()
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/loans/overdue", response_model=PaginatedResponse[Loan])
def get_overdue_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar empréstimos atrasados"""
    skip = (page - 1) * size
    service = LoanService(LoanRepository(db))
    loans = service.get_overdue_loans(skip, size)
    total = service.get_overdue_loans_count()
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/loans/{user_id}", response_model=PaginatedResponse[Loan])
def get_user_loans(user_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Consultar histórico de empréstimos por usuário"""
    skip = (page - 1) * size
    service = LoanService(LoanRepository(db))
    loans = service.get_user_loans(user_id, skip, size)
    total = service.get_user_loans_count(user_id)
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )
