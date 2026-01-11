from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import SessionLocal
from services.user_service import UserService
from repositories.user_repository import UserRepository
from schemas.user import User, UserCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

