from abc import ABC, abstractmethod
from src.domain.entities.client import Client, DBClient


class ClientRepository(ABC):
    @abstractmethod
    async def create(self, client: Client) -> DBClient:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> DBClient | None:
        pass
