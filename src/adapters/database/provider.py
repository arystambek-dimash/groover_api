from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repositories.client_repo import ClientRepositoryImpl
from src.adapters.database.repositories.staff_repo import StaffRepositoryImpl
from src.adapters.database.repositories.user_repo import UserRepositoryImpl
from src.adapters.database.uow import DBSession


def get_uow(session: AsyncSession) -> DBSession:
    return DBSession(session=session)


def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)


def get_staff_repository(session: AsyncSession) -> StaffRepositoryImpl:
    return StaffRepositoryImpl(session=session)


def get_client_repository(session: AsyncSession) -> ClientRepositoryImpl:
    return ClientRepositoryImpl(session=session)
