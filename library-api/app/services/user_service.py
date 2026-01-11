from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
import hashlib

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def create_user(self, user: UserCreate):
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        user_data = user.dict()
        user_data['hashed_password'] = hashed_password
        del user_data['password']
        
        return self.repository.create_with_password(user_data)

    def delete_user(self, user_id: int):
        return self.repository.delete(user_id)