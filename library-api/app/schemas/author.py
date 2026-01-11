from pydantic import BaseModel
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None
    nationality: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True