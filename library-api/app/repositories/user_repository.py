from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

