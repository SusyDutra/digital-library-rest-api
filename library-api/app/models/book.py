from sqlalchemy import Column, Integer, String, Text
from models import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    pages = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Book(name={self.name}, pages={self.pages})>"
