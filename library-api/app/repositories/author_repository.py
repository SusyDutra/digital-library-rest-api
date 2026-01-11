from sqlalchemy.orm import Session
from app.models.author import Author
from app.schemas.author import AuthorCreate

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

