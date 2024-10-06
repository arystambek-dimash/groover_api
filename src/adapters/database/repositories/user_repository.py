from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.database.models.user import UserOrm as UserORM
from src.domain.entities.user import User, DBUser
from src.domain.value_objects.user import UserEmail, UserPassword


class UserRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, item: User) -> DBUser:
        user_orm = UserORM(
            email=item.email.value,
            password=item.password.value,
            username=item.username,
            avatar_id=item.avatar_id
        )
        self.session.add(user_orm)
        await self.session.flush()
        await self.session.refresh(user_orm)
        return self._map_to_db_user(user_orm)

    async def get(self, item_id: int) -> Optional[DBUser]:
        query = select(UserORM).where(UserORM.id == item_id).options(
            selectinload(UserORM.client),
            selectinload(UserORM.staff),
            selectinload(UserORM.avatar)
        )
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()
        role = 'CLIENT'
        if user_orm and user_orm.staff:
            role = user_orm.staff.role.value
        return self._map_to_db_user(user_orm, role) if user_orm else None

    async def get_by_email(self, email: str) -> Optional[DBUser]:
        query = select(UserORM).where(UserORM.email == email).options(
            selectinload(UserORM.client),
            selectinload(UserORM.staff),
            selectinload(UserORM.avatar)
        )
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()
        role = 'CLIENT'
        if user_orm and user_orm.staff:
            role = user_orm.staff.role.value
        return self._map_to_db_user(user_orm, role) if user_orm else None

    async def list(self) -> List[DBUser]:
        query = select(UserORM).options(
            selectinload(UserORM.client),
            selectinload(UserORM.staff)
        )
        result = await self.session.execute(query)
        user_orms = result.scalars().all()
        return [self._map_to_db_user(user_orm) for user_orm in user_orms]

    async def update(self, item: DBUser) -> None:
        query = select(UserORM).where(UserORM.id == item.id)
        result = await self.session.execute(query)
        user_orm = result.scalar_one()
        if item.email:
            user_orm.email = item.email.value
        if item.password:
            user_orm.password = item.password.value
        if item.username:
            user_orm.username = item.username
        if item.avatar_id:
            user_orm.avatar_id = item.avatar_id
        await self.session.flush()

    async def delete(self, item_id: int) -> None:
        query = delete(UserORM).where(UserORM.id == item_id)
        await self.session.execute(query)
        await self.session.flush()

    @staticmethod
    def _map_to_db_user(user_orm: UserORM, role: str = None) -> DBUser:
        return DBUser(
            id=user_orm.id,
            email=UserEmail(user_orm.email),
            password=UserPassword(user_orm.password),
            username=user_orm.username,
            role=role,
            avatar_id=user_orm.avatar_id,
            avatar_url=user_orm.avatar.image_url if user_orm.avatar else None
        )
