from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import DBWorkout


@dataclass
class Tag:
    name: str


@dataclass(kw_only=True)
class DBTag(Tag):
    id: int
    usages: int


@dataclass(kw_only=True)
class DBTagWorkout(DBTag):
    workouts: List['DBWorkout']
