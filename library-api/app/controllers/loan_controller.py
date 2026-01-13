from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import SessionLocal
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import Loan, LoanCreate, LoanReturn
from app.schemas.pagination import PaginatedResponse
from app.logging_config import get_logger
import math

router = APIRouter()
logger = get_logger(__name__)

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
def get_loans(page: int = Query(1, ge=1, description="Page number"), size: int = Query(10, ge=1, le=100, description="Items per page"), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting loans list",
        request_id=request_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = LoanService(LoanRepository(db))
        loans = service.get_all_loans(skip, size)
        total = service.get_loans_count()
        pages = math.ceil(total / size)
        
        logger.info(
            "Loans retrieved successfully",
            request_id=request_id,
            total_loans=total,
            returned_count=len(loans)
        )
        
        return PaginatedResponse(
            items=loans,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting loans",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting loans",
            request_id=request_id,
            error=str(e)
        )
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
def create_loan(loan: LoanCreate, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Creating new loan",
        request_id=request_id,
        user_id=loan.user_id,
        book_id=loan.book_id
    )
    
    try:
        service = LoanService(LoanRepository(db))
        created_loan = service.create_loan(loan)
        
        logger.info(
            "Loan created successfully",
            request_id=request_id,
            loan_id=created_loan.id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            due_date=created_loan.due_date.isoformat() if created_loan.due_date else None
        )
        
        return created_loan
    except HTTPException as e:
        logger.warning(
            "Loan creation failed - business logic error",
            request_id=request_id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            error=e.detail,
            status_code=e.status_code
        )
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error creating loan",
            request_id=request_id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error creating loan",
            request_id=request_id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.put("/loans/{loan_id}/return", response_model=LoanReturn, responses={
    200: {"description": "Book returned successfully with fine calculation"},
    404: {"description": "Active loan not found"},
    500: {"description": "Internal server error"}
})
def return_book(loan_id: int, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Processing book return",
        request_id=request_id,
        loan_id=loan_id
    )
    
    try:
        service = LoanService(LoanRepository(db))
        loan = service.return_book(loan_id)
        
        logger.info(
            "Book returned successfully",
            request_id=request_id,
            loan_id=loan_id,
            fine_amount=float(loan.fine_amount) if loan.fine_amount else 0.0,
            return_date=loan.return_date.isoformat() if loan.return_date else None
        )
        
        return LoanReturn(
            fine_amount=loan.fine_amount,
            message=f"Book returned. Fine: R$ {loan.fine_amount:.2f}"
        )
    except HTTPException as e:
        logger.warning(
            "Book return failed",
            request_id=request_id,
            loan_id=loan_id,
            error=e.detail,
            status_code=e.status_code
        )
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error returning book",
            request_id=request_id,
            loan_id=loan_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error returning book",
            request_id=request_id,
            loan_id=loan_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/active", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with active loans"},
    500: {"description": "Internal server error"}
})
def get_active_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting active loans",
        request_id=request_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = LoanService(LoanRepository(db))
        loans = service.get_active_loans(skip, size)
        total = service.get_active_loans_count()
        pages = math.ceil(total / size)
        
        logger.info(
            "Active loans retrieved successfully",
            request_id=request_id,
            total_active_loans=total,
            returned_count=len(loans)
        )
        
        return PaginatedResponse(
            items=loans,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting active loans",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting active loans",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/overdue", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with overdue loans"},
    500: {"description": "Internal server error"}
})
def get_overdue_loans(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting overdue loans",
        request_id=request_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = LoanService(LoanRepository(db))
        loans = service.get_overdue_loans(skip, size)
        total = service.get_overdue_loans_count()
        pages = math.ceil(total / size)
        
        logger.info(
            "Overdue loans retrieved successfully",
            request_id=request_id,
            total_overdue_loans=total,
            returned_count=len(loans)
        )
        
        return PaginatedResponse(
            items=loans,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting overdue loans",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting overdue loans",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/loans/{user_id}", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "Successful response with user's loans"},
    404: {"description": "User not found"},
    500: {"description": "Internal server error"}
})
def get_user_loans(user_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting user loans by user ID",
        request_id=request_id,
        user_id=user_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = LoanService(LoanRepository(db))
        loans = service.get_user_loans(user_id, skip, size)
        total = service.get_user_loans_count(user_id)
        pages = math.ceil(total / size)
        
        logger.info(
            "User loans retrieved successfully",
            request_id=request_id,
            user_id=user_id,
            total_user_loans=total,
            returned_count=len(loans)
        )
        
        return PaginatedResponse(
            items=loans,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting user loans",
            request_id=request_id,
            user_id=user_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting user loans",
            request_id=request_id,
            user_id=user_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
