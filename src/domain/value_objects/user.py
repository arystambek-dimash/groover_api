from __future__ import annotations

import re
from dataclasses import dataclass, field

from asyncpg import InvalidPasswordError
from passlib.context import CryptContext

from src.domain.common.value_objects.base import ValueObject

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class UserEmail(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_regex, self.value):
            raise ValueError(f"Неверный формат электронной почты: {self.value}")


@dataclass(frozen=True)
class UserPassword:
    value: str = field(repr=False)

    MIN_LENGTH: int = 8

    def __post_init__(self):
        if not self.is_hashed(self.value):
            self._validate()
            hashed_password = _pwd_context.hash(self.value)
            object.__setattr__(self, 'value', hashed_password)

    def _validate(self) -> None:
        if len(self.value) < self.MIN_LENGTH:
            raise InvalidPasswordError(f"Пароль должен быть длиной минимум {self.MIN_LENGTH} символов.")

        if not re.search(r"[a-z]", self.value):
            raise InvalidPasswordError("Пароль должен содержать хотя бы одну строчную букву.")

        if not re.search(r"\d", self.value):
            raise InvalidPasswordError("Пароль должен содержать хотя бы одну цифру.")

    @staticmethod
    def is_hashed(password: str) -> bool:
        return password.startswith("$2b$")

    def verify(self, plain_password: str) -> bool:
        if not plain_password:
            raise InvalidPasswordError("Пароль для проверки не может быть пустым.")
        return _pwd_context.verify(plain_password, self.value)
