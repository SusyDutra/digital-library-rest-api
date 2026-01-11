from app.repositories.author_repository import AuthorRepository
from app.schemas.author import AuthorCreate

class AuthorService:
    def __init__(self, repository: AuthorRepository):
        self.repository = repository
