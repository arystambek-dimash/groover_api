from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.main.config import DBSettings


async def get_engine(settings: DBSettings) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        settings.db_uri
    )
    yield engine

    await engine.dispose()


async def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return session_factory
