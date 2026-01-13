from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import SessionLocal
from app.services.book_service import BookService
from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.book import Book, BookCreate, BookAvailability
from app.schemas.pagination import PaginatedResponse
import math

router = APIRouter()

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
def get_books(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    try:
        skip = (page - 1) * size
        service = BookService(BookRepository(db))
        books = service.get_all_books(skip, size)
        total = service.get_books_count()
        pages = math.ceil(total / size)
        
        return PaginatedResponse(
            items=books,
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

@router.post("/books", response_model=Book, responses={
    201: {"description": "Book created successfully"},
    400: {"description": "Invalid input data"},
    404: {"description": "Author not found"},
    500: {"description": "Internal server error"}
})
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        service = BookService(
            BookRepository(db), 
            AuthorRepository(db)
        )
        return service.create_book(book)
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

@router.get("/books/{book_id}/availability", response_model=BookAvailability, responses={
    200: {"description": "Book availability information"},
    404: {"description": "Book not found"},
    500: {"description": "Internal server error"}
})
def check_book_availability(book_id: int, db: Session = Depends(get_db)):
    try:
        service = BookService(BookRepository(db))
        return service.check_availability(book_id)
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

@router.get("/books/{book_id}", response_model=Book, responses={
    200: {"description": "Book details retrieved successfully"},
    404: {"description": "Book not found"},
    500: {"description": "Internal server error"}
})
def get_book(book_id: int, db: Session = Depends(get_db)):
    try:
        service = BookService(BookRepository(db))
        book = service.get_book(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book
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

