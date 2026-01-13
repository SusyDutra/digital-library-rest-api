from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import SessionLocal
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.book import Book, BookCreate, BookAvailability
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

@router.get("/books", response_model=PaginatedResponse[Book], responses={
    200: {"description": "Successful response with paginated books"},
    500: {"description": "Internal server error"}
})
def get_books(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting books list",
        request_id=request_id,
        page=page,
        size=size
    )
    
    try:
        skip = (page - 1) * size
        service = BookService(BookRepository(db))
        books = service.get_all_books(skip, size)
        total = service.get_books_count()
        pages = math.ceil(total / size)
        
        logger.info(
            "Books retrieved successfully",
            request_id=request_id,
            total_books=total,
            returned_count=len(books)
        )
        
        return PaginatedResponse(
            items=books,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting books",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting books",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/books", response_model=Book, responses={
    201: {"description": "Book created successfully"},
    400: {"description": "Invalid input data"},
    404: {"description": "Author not found"},
    500: {"description": "Internal server error"}
})
def create_book(book: BookCreate, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Creating new book",
        request_id=request_id,
        book_name=book.name,
        author_id=book.author_id
    )
    
    try:
        service = BookService(
            BookRepository(db), 
            AuthorRepository(db)
        )
        created_book = service.create_book(book)
        
        logger.info(
            "Book created successfully",
            request_id=request_id,
            book_id=created_book.id,
            book_name=created_book.name
        )
        
        return created_book
    except HTTPException as e:
        logger.warning(
            "Book creation failed - business logic error",
            request_id=request_id,
            error=e.detail,
            status_code=e.status_code
        )
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error creating book",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error creating book",
            request_id=request_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/books/{book_id}/availability", response_model=BookAvailability, responses={
    200: {"description": "Book availability information"},
    404: {"description": "Book not found"},
    500: {"description": "Internal server error"}
})
def check_book_availability(book_id: int, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Checking book availability",
        request_id=request_id,
        book_id=book_id
    )
    
    try:
        service = BookService(BookRepository(db))
        availability = service.check_availability(book_id)
        
        logger.info(
            "Book availability checked",
            request_id=request_id,
            book_id=book_id,
            available=availability.available
        )
        
        return availability
    except HTTPException as e:
        logger.warning(
            "Book availability check failed",
            request_id=request_id,
            book_id=book_id,
            error=e.detail,
            status_code=e.status_code
        )
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error checking availability",
            request_id=request_id,
            book_id=book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error checking availability",
            request_id=request_id,
            book_id=book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/books/{book_id}", response_model=Book, responses={
    200: {"description": "Book details retrieved successfully"},
    404: {"description": "Book not found"},
    500: {"description": "Internal server error"}
})
def get_book(book_id: int, db: Session = Depends(get_db), request: Request = None):
    request_id = getattr(request.state, 'request_id', None) if request else None
    
    logger.info(
        "Getting book details",
        request_id=request_id,
        book_id=book_id
    )
    
    try:
        service = BookService(BookRepository(db))
        book = service.get_book(book_id)
        if not book:
            logger.warning(
                "Book not found",
                request_id=request_id,
                book_id=book_id
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        logger.info(
            "Book details retrieved",
            request_id=request_id,
            book_id=book_id,
            book_name=book.name
        )
        
        return book
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(
            "Database error getting book",
            request_id=request_id,
            book_id=book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(
            "Unexpected error getting book",
            request_id=request_id,
            book_id=book_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

