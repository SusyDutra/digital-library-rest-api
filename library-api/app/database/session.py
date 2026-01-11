# database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://library_user:library_pass@localhost:5432/library"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # evita conexões mortas
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)