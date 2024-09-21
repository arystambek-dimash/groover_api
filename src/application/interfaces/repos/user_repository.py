from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User, DBUser
from src.domain.value_objects.user import UserEmail


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[DBUser]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[DBUser]:
        pass

    @abstractmethod
    async def create(self, user: User) -> DBUser:
        pass

    @abstractmethod
    async def update(self, user: DBUser) -> None:
        pass
