from passlib.context import CryptContext

from src.application.user.dto import CreateUserDTO
from src.domain.entities.user import User
from src.domain.exceptions.user import InvalidEmailError
from src.domain.value_objects.user import UserEmail, UserPassword


class UserService:
    def create_user(self, email: str, password: str) -> User:
        try:
            email_vo = UserEmail(email)
        except ValueError as e:
            raise InvalidEmailError(str(e))

        password_vo = UserPassword(password)
        return User(
            email=email_vo,
            password=password_vo
        )

    def verify_password(self, plain_password: str, user_password: UserPassword) -> bool:
        return user_password.verify(plain_password)
