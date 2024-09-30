from dataclasses import asdict
from typing import List

from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.models import AvatarOrm
from src.domain.entities.avatar import Avatar, DBAvatar


class AvatarRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, avatar_id: int) -> DBAvatar:
        avatar = await self._session.get(AvatarOrm, avatar_id)
        return self._map_to_entity(avatar) if avatar else None

    async def add(self, avatar: Avatar) -> DBAvatar:
        stmt = insert(AvatarOrm).values(**asdict(avatar)).returning(AvatarOrm)
        result = await self._session.execute(stmt)
        response_entity = result.scalar_one()
        return self._map_to_entity(response_entity)

    async def list(self) -> List[DBAvatar]:
        stmt = select(AvatarOrm)
        result = await self._session.execute(stmt)
        return [self._map_to_entity(avatar) for avatar in result.scalars().all()]

    async def update(self, avatar: DBAvatar) -> DBAvatar:
        stmt = update(AvatarOrm).values(**asdict(avatar)).where(AvatarOrm.id == avatar.id).returning(AvatarOrm)
        result = await self._session.execute(stmt)
        response_entity = result.scalar_one()
        return self._map_to_entity(response_entity)

    async def delete(self, avatar_id: int) -> None:
        stmt = delete(AvatarOrm).where(AvatarOrm.id == avatar_id)
        await self._session.execute(stmt)

    @staticmethod
    def _map_to_entity(avatar: AvatarOrm) -> DBAvatar:
        return DBAvatar(
            id=avatar.id,
            image_url=avatar.image_url,
        )
