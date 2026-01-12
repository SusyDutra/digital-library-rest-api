from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
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

@router.get("/books", response_model=PaginatedResponse[Book])
def get_books(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Listar livros"""
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

@router.post("/books", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Cadastrar novo livro vinculado a um autor"""
    service = BookService(
        BookRepository(db), 
        AuthorRepository(db)
    )
    return service.create_book(book)

@router.get("/books/{book_id}/availability", response_model=BookAvailability)
def check_book_availability(book_id: int, db: Session = Depends(get_db)):
    """Verificar disponibilidade para empréstimo"""
    service = BookService(BookRepository(db))
    return service.check_availability(book_id)

@router.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Verificar livro por ID"""
    service = BookService(BookRepository(db))
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
