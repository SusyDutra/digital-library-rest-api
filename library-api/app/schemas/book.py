from pydantic import BaseModel
from typing import Optional
from app.schemas.author import Author

class BookBase(BaseModel):
    name: str
    description: Optional[str] = None
    pages: int
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author: Optional[Author] = None

    class Config:
        from_attributes = True

class BookAvailability(BaseModel):
    book_id: int
    name: str
    available: bool
    current_loan_id: Optional[int] = None