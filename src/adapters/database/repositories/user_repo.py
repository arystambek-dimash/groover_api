from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.database.models.user import UserOrm as UserORM
from src.application.interfaces.repos.user_repository import UserRepository
from src.domain.entities.user import User, DBUser
from src.domain.value_objects.user import UserEmail, UserPassword


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[DBUser]:
        query = select(UserORM).where(UserORM.id == user_id).options(
            selectinload(UserORM.client),
            selectinload(UserORM.staff)
        )
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()
        return self._map_to_db_user(user_orm) if user_orm else None

    async def get_by_email(self, email: str) -> Optional[DBUser]:
        query = select(UserORM).where(UserORM.email == email).options(
            selectinload(UserORM.client),
            selectinload(UserORM.staff)
        )
        result = await self.session.execute(query)
        user_orm = result.scalar_one_or_none()
        return self._map_to_db_user(user_orm) if user_orm else None

    async def create(self, user: User) -> DBUser:
        user_orm = UserORM(
            email=user.email.value,
            password=user.password.value,
            username=user.username,
            profile_image=user.profile_image
        )
        self.session.add(user_orm)
        await self.session.flush()
        await self.session.refresh(user_orm)
        return self._map_to_db_user(user_orm)

    async def update(self, user: DBUser) -> None:
        query = select(UserORM).where(UserORM.id == user.id)
        result = await self.session.execute(query)
        user_orm = result.scalar_one()
        user_orm.password = user.password.value
        user_orm.username = user.username
        user_orm.profile_image = user.profile_image
        await self.session.flush()

    def _map_to_db_user(self, user_orm: UserORM) -> DBUser:
        return DBUser(
            id=user_orm.id,
            email=UserEmail(user_orm.email),
            password=UserPassword(user_orm.password),
            username=user_orm.username,
            profile_image=user_orm.profile_image,
        )
