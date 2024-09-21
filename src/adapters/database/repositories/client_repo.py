from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.models.client import ClientOrm as ClientORM
from src.application.interfaces.repos.client_repository import ClientRepository
from src.domain.entities.client import Client, DBClient


class ClientRepositoryImpl(ClientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, client: Client) -> DBClient:
        client_orm = ClientORM(
            user_id=client.user.id,
        )
        self.session.add(client_orm)
        await self.session.flush()
        return DBClient(
            id=client_orm.id,
            user=client.user,
        )

    async def get_by_user_id(self, user_id: int) -> DBClient | None:
        result = await self.session.execute(
            select(ClientORM).where(ClientORM.user_id == user_id)
        )
        client_orm = result.scalar_one_or_none()
        if client_orm:
            return DBClient(
                id=client_orm.id,
                user=client_orm.user,
            )
        return None
