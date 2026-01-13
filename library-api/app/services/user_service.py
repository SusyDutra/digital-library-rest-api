from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.logging_config import get_logger
import hashlib

logger = get_logger(__name__)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self, skip: int = 0, limit: int = 10):
        logger.debug("Fetching all users from repository", skip=skip, limit=limit)
        return self.repository.get_all(skip, limit)

    def get_users_count(self):
        count = self.repository.get_total_count()
        logger.debug("Retrieved users count", total_count=count)
        return count

    def get_user(self, user_id: int):
        logger.debug("Fetching user by ID", user_id=user_id)
        return self.repository.get_by_id(user_id)

    def create_user(self, user: UserCreate):
        logger.info("Creating user", user_name=user.name, user_email=user.email)
        
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        user_data = user.dict()
        user_data['hashed_password'] = hashed_password
        del user_data['password']
        
        logger.debug("Password hashed for user", user_email=user.email)
        
        created_user = self.repository.create(user_data)
        logger.info("User created successfully", user_id=created_user.id, user_name=created_user.name, user_email=created_user.email)
        return created_user

    def delete_user(self, user_id: int):
        logger.info("Deleting user", user_id=user_id)
        deleted_user = self.repository.delete(user_id)
        if deleted_user:
            logger.info("User deleted successfully", user_id=user_id)
        else:
            logger.warning("User not found for deletion", user_id=user_id)
        return deleted_user