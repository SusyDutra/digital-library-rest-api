from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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

@router.get("/loans", response_model=PaginatedResponse[Loan], summary="List all loans", description="Retrieve a paginated list of all loans (active and historical)", responses={
    200: {"description": "Successful response with paginated loans"},
    500: {"description": "Internal server error"}
})
def get_loans(page: int = Query(1, ge=1, description="Page number"), size: int = Query(10, ge=1, le=100, description="Items per page"), db: Session = Depends(get_db)):
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/loans", response_model=Loan, responses={
    201: {"description": "Loan created successfully"},
    400: {"description": "Book not available or user has 3 active loans"},
    404: {"description": "Book or user not found"},
    500: {"description": "Internal server error"}
})
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    try:
        service = LoanService(LoanRepository(db))
        return service.create_loan(loan)
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/loans/{loan_id}/return", response_model=LoanReturn, responses={
    200: {"description": "Book returned successfully with fine calculation"},
    404: {"description": "Active loan not found"},
    500: {"description": "Internal server error"}
})
def return_book(loan_id: int, db: Session = Depends(get_db)):
    try:
        service = LoanService(LoanRepository(db))
        loan = service.return_book(loan_id)
        return LoanReturn(
            fine_amount=loan.fine_amount,
            message=f"Book returned. Fine: R$ {loan.fine_amount:.2f}"
        )
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/active", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with active loans"},
    500: {"description": "Internal server error"}
})
def get_active_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/overdue", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with overdue loans"},
    500: {"description": "Internal server error"}
})
def get_overdue_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
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
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/{user_id}", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with user's loans"},
    404: {"description": "User not found"},
    500: {"description": "Internal server error"}
})
def get_user_loans(user_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
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
    except HTTPException:
        raise
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
