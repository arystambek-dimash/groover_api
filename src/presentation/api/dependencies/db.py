from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.presentation.interactor_factory import InteractorFactory


async def get_session_factory(
        ioc: InteractorFactory = Depends()
) -> async_sessionmaker[AsyncSession]:
    return ioc.get_session_factory()


async def get_db_session(
        session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory)
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
