from sqlalchemy import Column, Integer, String, Text
from models import Base

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)

    author = relationship("Author")

    def __repr__(self):
        return f"<Book(name={self.name}, pages={self.pages})>"
