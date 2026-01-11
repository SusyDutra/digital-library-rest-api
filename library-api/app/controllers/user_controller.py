from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.repositories.user_repository import UserRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.user import UserResponse, UserCreate
from app.schemas.loan import Loan

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Listar todos os usuários"""
    service = UserService(UserRepository(db))
    return service.get_all_users()

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Buscar usuário por ID"""
    service = UserService(UserRepository(db))
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Cadastrar novo usuário"""
    service = UserService(UserRepository(db))
    return service.create_user(user)

@router.get("/users/{user_id}/loans", response_model=list[Loan])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    """Listar todos os empréstimos associados a um usuário"""

    user_service = UserService(UserRepository(db))
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    loan_service = LoanService(LoanRepository(db))
    return loan_service.get_user_loans(user_id)

