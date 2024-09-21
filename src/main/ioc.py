from contextlib import asynccontextmanager
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.adapters.auth.jwt_service import JWTService
from src.adapters.database.provider import get_user_repository, get_uow, get_staff_repository, get_client_repository
from src.application.user.user_interactor import UserInteractor
from src.domain.services.user import UserService
from src.main.web import settings

from src.presentation.interactor_factory import (
    InteractorFactory,
    InteractorPicker,
    GenericInputDTO,
    GenericOutputDTO,
    InteractorCallable)


class IoC(InteractorFactory):
    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory
        self._user_service = UserService()
        self._jwt_service = JWTService(settings.jwt.jwt_secret_key)

    def _construct_user_interactor(
            self, session: AsyncSession
    ) -> UserInteractor:
        user_repository = get_user_repository(session)
        staff_repository = get_staff_repository(session)
        client_repository = get_client_repository(session)
        uow = get_uow(session)
        return UserInteractor(
            user_repository=user_repository,
            uow=uow,
            user_service=self._user_service,
            jwt_service=self._jwt_service,
            staff_repository=staff_repository,
            client_repository=client_repository
        )

    @asynccontextmanager
    async def pick_user_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncIterator[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        async with self._session_factory() as session:
            interactor = self._construct_user_interactor(session)
            yield picker(interactor)

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
