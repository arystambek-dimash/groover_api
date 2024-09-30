from typing import Protocol, TypeVar, List, Optional, Union

from src.domain.entities.avatar import DBAvatar
from src.domain.entities.staff import DBStaff
from src.domain.entities.style import DBStyle, DBStyleWorkout
from src.domain.entities.tag import DBTag, DBTagWorkout
from src.domain.entities.user import DBUser
from src.domain.entities.workout import DBWorkout

T = TypeVar('T')


class Repository(Protocol[T]):
    async def add(self, item: T) -> T:
        ...

    async def get(self, item_id: int) -> T | None:
        ...

    async def list(self) -> List[T]:
        ...

    async def update(self, item: T) -> T:
        ...

    async def delete(self, item_id: int) -> None:
        ...


class UserRepository(Repository[DBUser], Protocol):
    async def get_by_email(self, email: str) -> DBUser:
        ...


class RoleRepository(Repository[DBStaff], Protocol):
    async def get_by_user_id(self, user_id: int) -> DBStaff:
        ...


class StyleRepository(Repository[Union[DBStyleWorkout, DBStyle]], Protocol):
    async def get_with_workouts(self, style_id: int) -> DBStyleWorkout | None:
        ...

    async def get_by_name(self, name: str) -> DBStyle | None:
        ...


class TagRepository(Repository[Union[DBTag, DBTagWorkout]], Protocol):
    async def get_with_workouts(self, tag_id: int) -> DBTagWorkout | None:
        ...

    async def get_by_name(self, name: str) -> DBTag | None:
        ...

    async def increment_usages(self, tag_id: int) -> int:
        ...

    async def decrement_usages(self, tag_id: int) -> int:
        ...

    async def search_by_constraints(self,
                                    name: Optional[str] = None,
                                    min_usages: Optional[int] = None,
                                    max_usages: Optional[int] = None,
                                    with_workout: Optional[bool] = False
                                    ):
        ...


class WorkoutRepository(Repository[DBWorkout], Protocol):
    async def get_with_style(self, style_id: int, with_workouts: bool) -> DBWorkout | None:
        ...

    async def get_by_name(self, name: str) -> DBWorkout | None:
        ...


class AvatarRepository(Repository[DBAvatar], Protocol):
    ...


class WorkoutTagAssociationRepository(Protocol):
    async def insert_workout_tag_association(self, workout_id: int, tag_id: int):
        ...

    async def delete_workout_tag_association(self, workout_id: int, tag_id: int):
        ...

    async def get_workout_tag_association(self, workout_id: int, tag_id: int):
        ...

    async def get_by_workout_id(self, workout_id: int):
        ...
