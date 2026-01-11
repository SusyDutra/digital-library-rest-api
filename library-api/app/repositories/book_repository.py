from sqlalchemy.orm import Session
from models.book import Book
from schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

