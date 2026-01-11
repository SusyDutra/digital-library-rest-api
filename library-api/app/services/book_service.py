from repositories.book_repository import BookRepository
from schemas.book import BookCreate

class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

