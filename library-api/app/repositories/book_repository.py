from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.loan import Loan
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Book).all()

    def get_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def create(self, book: BookCreate):
        db_book = Book(**book.dict())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def delete(self, book_id: int):
        book = self.get_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
        return book

    def check_availability(self, book_id: int):
        active_loan = self.db.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.status == "active"
        ).first()
        return {
            "available": active_loan is None,
            "current_loan_id": active_loan.id if active_loan else None
        }