from repositories.user_repository import UserRepository
from schemas.user import UserCreate

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
