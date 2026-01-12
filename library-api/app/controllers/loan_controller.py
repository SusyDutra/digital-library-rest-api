from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import Loan, LoanCreate, LoanReturn

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@router.get("/loans/active", response_model=list[Loan])
def get_active_loans(db: Session = Depends(get_db)):
    """Listar empréstimos ativos"""
    service = LoanService(LoanRepository(db))
    return service.get_active_loans()

@router.get("/loans/overdue", response_model=list[Loan])
def get_overdue_loans(db: Session = Depends(get_db)):
    """Listar empréstimos atrasados"""
    service = LoanService(LoanRepository(db))
    return service.get_overdue_loans()

@router.get("/loans/{user_id}", response_model=list[Loan])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    """Consultar histórico de empréstimos por usuário"""
    service = LoanService(LoanRepository(db))
    return service.get_user_loans(user_id)

@router.get("/loans", response_model=list[Loan])
def get_loans(db: Session = Depends(get_db)):
    service = LoanService(LoanRepository(db))
    return service.get_all_loans()

