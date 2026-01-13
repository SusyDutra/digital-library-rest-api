from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.database.session import SessionLocal
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.repositories.user_repository import UserRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.user import UserResponse, UserCreate
from app.schemas.loan import Loan
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

@router.get("/users", response_model=PaginatedResponse[UserResponse], responses={
    200: {"description": "Successful response with paginated users"},
    500: {"description": "Internal server error"}
})
def get_users(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting users list",
        request_id=request_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = UserService(UserRepository(db))
        users = service.get_all_users(skip, size)
        total = service.get_users_count()
        pages = math.ceil(total / size)
        
        logger.info(
            "Users retrieved successfully",
            request_id=request_id,
            total_users=total,
            returned_count=len(users)
        )
        
        return PaginatedResponse(
            items=users,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting users",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting users",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/users", response_model=UserResponse, responses={
    201: {"description": "User created successfully"},
    400: {"description": "Invalid input data or email already exists"},
    500: {"description": "Internal server error"}
})
def create_user(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Creating new user",
        request_id=request_id,
        user_name=user.name,
        user_email=user.email
    )
    
    try:
        service = UserService(UserRepository(db))
        created_user = service.create_user(user)
        
        logger.info(
            "User created successfully",
            request_id=request_id,
            user_id=created_user.id,
            user_name=created_user.name,
            user_email=created_user.email
        )
        
        return created_user
    except IntegrityError as e:
        logger.warning(
            "User creation failed - email already exists",
            request_id=request_id,
            user_email=user.email,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error creating user",
            request_id=request_id,
            user_email=user.email,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error creating user",
            request_id=request_id,
            user_email=user.email,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/users/{user_id}", response_model=UserResponse, responses={
    200: {"description": "User details retrieved successfully"},
    404: {"description": "User not found"},
    500: {"description": "Internal server error"}
})
def get_user(user_id: int, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting user details",
        request_id=request_id,
        user_id=user_id
    )
    
    try:
        service = UserService(UserRepository(db))
        user = service.get_user(user_id)
        if not user:
            logger.warning(
                "User not found",
                request_id=request_id,
                user_id=user_id
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(
            "User details retrieved",
            request_id=request_id,
            user_id=user_id,
            user_name=user.name
        )
        
        return user
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting user",
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
            "Unexpected error getting user",
            request_id=request_id,
            user_id=user_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/users/{user_id}/loans", response_model=PaginatedResponse[Loan], responses={
    200: {"description": "User's loan history retrieved successfully"},
    404: {"description": "User not found"},
    500: {"description": "Internal server error"}
})
def get_user_loans(user_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting user loan history",
        request_id=request_id,
        user_id=user_id,
        page=page,
        size=size
    )
    
    try:
        user_service = UserService(UserRepository(db))
        user = user_service.get_user(user_id)
        if not user:
            logger.warning(
                "User not found for loan history",
                request_id=request_id,
                user_id=user_id
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        skip = (page - 1) * size
        loan_service = LoanService(LoanRepository(db))
        loans = loan_service.get_user_loans(user_id, skip, size)
        total = loan_service.get_user_loans_count(user_id)
        pages = math.ceil(total / size)
        
        logger.info(
            "User loan history retrieved",
            request_id=request_id,
            user_id=user_id,
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
