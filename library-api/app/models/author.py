from sqlalchemy import Column, Integer, String, Text
from app.models import Base

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    biography = Column(Text, nullable=True)
    nationality = Column(String(100), nullable=True)