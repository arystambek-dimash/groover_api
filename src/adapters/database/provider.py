from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repositories.avatar_repository import AvatarRepository
from src.adapters.database.repositories.client_repository import ClientRepositoryImpl
from src.adapters.database.repositories.staff_repository import StaffRepositoryImpl
from src.adapters.database.repositories.style_respository import StyleRepositoryImpl
from src.adapters.database.repositories.tag_repository import TagRepositoryImpl
from src.adapters.database.repositories.user_repository import UserRepositoryImpl
from src.adapters.database.repositories.workout_repository import WorkoutRepositoryImpl
from src.adapters.database.repositories.workout_tag_repository import WorkoutTagAssociationRepository
from src.adapters.database.uow import DBSession


def get_uow(session: AsyncSession) -> DBSession:
    return DBSession(session=session)


def get_user_repository(session: AsyncSession) -> UserRepositoryImpl:
    return UserRepositoryImpl(session=session)


def get_staff_repository(session: AsyncSession) -> StaffRepositoryImpl:
    return StaffRepositoryImpl(session=session)


def get_client_repository(session: AsyncSession) -> ClientRepositoryImpl:
    return ClientRepositoryImpl(session=session)


def get_style_repository(session: AsyncSession) -> StyleRepositoryImpl:
    return StyleRepositoryImpl(session=session)


def get_tag_repository(session: AsyncSession) -> TagRepositoryImpl:
    return TagRepositoryImpl(session=session)


def get_workout_repository(session: AsyncSession) -> WorkoutRepositoryImpl:
    return WorkoutRepositoryImpl(session=session)


def get_workout_tag_repository(session: AsyncSession) -> WorkoutTagAssociationRepository:
    return WorkoutTagAssociationRepository(session=session)


def get_avatar_repository(session: AsyncSession) -> AvatarRepository:
    return AvatarRepository(session=session)
