from app.repositories.book_repository import BookRepository
from app.repositories.author_repository import AuthorRepository
from app.schemas.book import BookCreate
from fastapi import HTTPException

class BookService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository = None):
        self.book_repository = book_repository
        self.author_repository = author_repository

    def get_all_books(self):
        return self.book_repository.get_all()

    def get_book(self, book_id: int):
        return self.book_repository.get_by_id(book_id)

    def create_book(self, book: BookCreate):
        # Verificar se autor existe
        if self.author_repository:
            author = self.author_repository.get_by_id(book.author_id)
            if not author:
                raise HTTPException(status_code=404, detail="Author not found")
        
        return self.book_repository.create(book)

    # def delete_book(self, book_id: int):
    #     return self.book_repository.delete(book_id)

    def check_availability(self, book_id: int):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        availability_info = self.book_repository.check_availability(book_id)
        return {
            "book_id": book_id,
            "name": book.name,
            "available": availability_info["available"],
            "current_loan_id": availability_info["current_loan_id"]
        }