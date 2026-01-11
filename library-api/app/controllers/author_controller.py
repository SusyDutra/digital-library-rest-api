from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.author_service import AuthorService
from app.repositories.author_repository import AuthorRepository
from app.schemas.author import Author, AuthorCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
