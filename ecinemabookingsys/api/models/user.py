from abc import ABC, abstractmethod
from models.base import BaseModel
from services.user_service import UserService


class User(BaseModel, ABC):
    def __init__(self, user_id=None, password=None, email=None, **kwargs):
        self.user_id = user_id
        self.password = password
        self.email = email

        # Handle extra fields
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def to_dict(self):
        pass

    def check_password(self, password):
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def change_password(self, new_password, first_name='there'):
        UserService.change_password(self.user_id, self.email, new_password, first_name)
        import bcrypt
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def login(cls, email, password):
        return UserService.login(email, password)

    @staticmethod
    def logout(session):
        session.clear()

    @classmethod
    def find_by_id(cls, user_id):
        return UserService.get_user_by_id(user_id)

    @classmethod
    def find_by_email(cls, email):
        return UserService.get_user_by_email(email)

    def activate(self):
        UserService.activate_user(self.user_id)
