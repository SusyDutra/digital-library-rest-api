from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.repositories.user_repository import UserRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.user import UserResponse, UserCreate
from app.schemas.loan import Loan
from app.schemas.pagination import PaginatedResponse
import math

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=PaginatedResponse[UserResponse])
def get_users(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar todos os usuários"""
    skip = (page - 1) * size
    service = UserService(UserRepository(db))
    users = service.get_all_users(skip, size)
    total = service.get_users_count()
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Cadastrar novo usuário"""
    service = UserService(UserRepository(db))
    return service.create_user(user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Buscar usuário por ID"""
    service = UserService(UserRepository(db))
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}/loans", response_model=PaginatedResponse[Loan])
def get_user_loans(user_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar todos os empréstimos associados a um usuário"""
    user_service = UserService(UserRepository(db))
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skip = (page - 1) * size
    loan_service = LoanService(LoanRepository(db))
    loans = loan_service.get_user_loans(user_id, skip, size)
    total = loan_service.get_user_loans_count(user_id)
    pages = math.ceil(total / size)
    
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        size=size,
        pages=pages
    )
