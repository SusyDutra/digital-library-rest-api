from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    name: str
    description: Optional[str] = None
    pages: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True