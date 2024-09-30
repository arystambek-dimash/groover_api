from typing import Optional
from src.domain.entities.user import User
from src.domain.exceptions.user import InvalidEmailError, InvalidPasswordError
from src.domain.value_objects.user import UserEmail, UserPassword


class UserService:
    @staticmethod
    def create_user(email: str, password: str) -> User:
        try:
            email_vo = UserEmail(email)
        except ValueError as e:
            raise InvalidEmailError(str(e))

        try:
            password_vo = UserPassword(password)
        except ValueError as e:
            raise InvalidPasswordError(str(e))

        return User(email=email_vo, password=password_vo, avatar_id=None)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return UserPassword(hashed_password).verify(plain_password)

    @staticmethod
    def update_user(
            user: User,
            password: Optional[str] = None,
            username: Optional[str] = None,
            avatar_id: Optional[int] = None,
    ) -> User:
        if password:
            try:
                user.password = UserPassword(password)
            except ValueError as e:
                raise InvalidPasswordError(str(e))

        if username is not None:
            user.username = username
        if avatar_id is not None:
            user.avatar_id = avatar_id
        return user
