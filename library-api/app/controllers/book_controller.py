from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import SessionLocal
from services.book_service import BookService
from repositories.book_repository import BookRepository
from schemas.book import Book, BookCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

