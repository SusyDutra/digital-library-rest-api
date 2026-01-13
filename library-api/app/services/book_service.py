from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.book import BookCreate
from app.logging_config import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

class BookService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository = None):
        self.book_repository = book_repository
        self.author_repository = author_repository

    def get_all_books(self, skip: int = 0, limit: int = 10):
        logger.debug("Fetching books from repository", skip=skip, limit=limit)
        return self.book_repository.get_all(skip, limit)

    def get_books_count(self):
        count = self.book_repository.get_total_count()
        logger.debug("Retrieved books count", total_count=count)
        return count

    def get_book(self, book_id: int):
        logger.debug("Fetching book by ID", book_id=book_id)
        return self.book_repository.get_by_id(book_id)

    def create_book(self, book: BookCreate):
        logger.info("Creating book", book_name=book.name, author_id=book.author_id)
        
        # Verificar se autor existe
        if self.author_repository:
            author = self.author_repository.get_by_id(book.author_id)
            if not author:
                logger.warning("Author not found for book creation", author_id=book.author_id)
                raise HTTPException(status_code=404, detail="Author not found")
            logger.debug("Author validated", author_id=book.author_id, author_name=author.name)
        
        created_book = self.book_repository.create(book)
        logger.info("Book created successfully", book_id=created_book.id, book_name=created_book.name)
        return created_book

    def check_availability(self, book_id: int):
        logger.debug("Checking book availability", book_id=book_id)
        
        book = self.book_repository.get_by_id(book_id)
        if not book:
            logger.warning("Book not found for availability check", book_id=book_id)
            raise HTTPException(status_code=404, detail="Book not found")
        
        availability_info = self.book_repository.check_availability(book_id)
        
        logger.info(
            "Book availability checked",
            book_id=book_id,
            available=availability_info["available"],
            current_loan_id=availability_info["current_loan_id"]
        )
        
        return {
            "book_id": book_id,
            "name": book.name,
            "available": availability_info["available"],
            "current_loan_id": availability_info["current_loan_id"]
        }