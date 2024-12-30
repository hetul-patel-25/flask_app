from app.models.user_model import User
from app.repository.crud_repository import CrudRepository

class AuthRepository(CrudRepository):
    def __init__(self):
        super().__init__(User)