from contextlib import asynccontextmanager
from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.avatar.interactor import AvatarInteractor
from src.application.interfaces.interactor import Interactor
from src.application.tag.interactor import TagInteractor
from src.application.workout.interactor import WorkoutInteractor
from src.domain.services.avatar import AvatarService
from src.domain.services.upload import UploadService
from src.domain.services.workout import WorkoutService
from src.main.web import settings
from src.application.user.jwt import JWTService
from src.adapters.database.provider import (
    get_uow,
    get_tag_repository,
    get_user_repository,
    get_style_repository,
    get_staff_repository,
    get_client_repository,
    get_workout_repository, get_workout_tag_repository, get_avatar_repository
)
from src.domain.services.tag import TagService
from src.domain.services.user import UserService
from src.domain.services.style import StyleService
from src.application.user.interactor import UserInteractor
from src.application.style.interactor import StyleInteractor
from src.presentation.interactor_factory import (
    InteractorFactory,
    InteractorPicker,
    GenericInputDTO,
    GenericOutputDTO,
    InteractorCallable
)


class IoC(InteractorFactory):
    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory
        self._jwt_service = JWTService(settings.jwt.jwt_secret_key)
        self._uow_factory = get_uow
        self._user_service = UserService()
        self._style_service = StyleService()
        self._workout_service = WorkoutService()
        self._avatar_service = AvatarService()
        self._tag_service = TagService()
        self._upload_service = UploadService()

    def _construct_user_interactor(
            self, session: AsyncSession
    ) -> UserInteractor:
        user_repository = get_user_repository(session)
        avatar_repository = get_avatar_repository(session)
        staff_repository = get_staff_repository(session)
        client_repository = get_client_repository(session)
        return UserInteractor(
            user_repository=user_repository,
            avatar_repository=avatar_repository,
            uow=self._uow_factory(session),
            user_service=self._user_service,
            jwt_service=self._jwt_service,
            staff_repository=staff_repository,
            client_repository=client_repository
        )

    def _construct_style_interactor(self, session: AsyncSession) -> StyleInteractor:
        style_repository = get_style_repository(session)
        uow = self._uow_factory(session)
        return StyleInteractor(
            uow=uow,
            style_repository=style_repository,
            style_service=self._style_service,
            upload_service=self._upload_service
        )

    def _construct_tag_interactor(self, session: AsyncSession) -> TagInteractor:
        tag_repository = get_tag_repository(session)
        uow = self._uow_factory(session)
        return TagInteractor(
            uow=uow,
            tag_repository=tag_repository,
            tag_service=self._tag_service
        )

    def _construct_workout_interactor(self, session: AsyncSession) -> WorkoutInteractor:
        tag_repository = get_tag_repository(session)
        style_repository = get_style_repository(session)
        workout_repository = get_workout_repository(session)
        workout_tag_repository = get_workout_tag_repository(session)
        uow = self._uow_factory(session)
        return WorkoutInteractor(
            workout_repository=workout_repository,
            workout_service=self._workout_service,
            workout_tag_association_repository=workout_tag_repository,
            tag_service=self._tag_service,
            tag_repository=tag_repository,
            style_repository=style_repository,
            upload_service=self._upload_service,
            uow=uow
        )

    def _construct_avatar_interactor(self, session: AsyncSession) -> AvatarInteractor:
        avatar_repository = get_avatar_repository(session)
        uow = self._uow_factory(session)
        return AvatarInteractor(
            avatar_repository=avatar_repository,
            uow=uow,
            avatar_service=self._avatar_service,
            upload_service=self._upload_service
        )

    def _pick_interactor(
            self,
            constructor: Callable[[AsyncSession], Interactor],
            picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        @asynccontextmanager
        async def manager():
            async with self._session_factory() as session:
                interactor = constructor(session)
                yield picker(interactor)

        return manager()

    def pick_user_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        return self._pick_interactor(self._construct_user_interactor, picker)

    def pick_style_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        return self._pick_interactor(self._construct_style_interactor, picker)

    def pick_tag_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        return self._pick_interactor(self._construct_tag_interactor, picker)

    def pick_workout_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        return self._pick_interactor(self._construct_workout_interactor, picker)

    def pick_avatar_interactor(
            self, picker: InteractorPicker[GenericInputDTO, GenericOutputDTO]
    ) -> AsyncContextManager[InteractorCallable[GenericInputDTO, GenericOutputDTO]]:
        return self._pick_interactor(self._construct_avatar_interactor, picker)

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
