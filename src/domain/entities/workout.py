from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from src.domain.entities.style import DBStyle
from src.domain.entities.tag import DBTag
from src.domain.value_objects.workout import LevelsEnum


@dataclass
class Workout:
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: str
    author_name: str
    views_count: int
    style_id: int
    tags: List[str]


@dataclass(kw_only=True)
class DBWorkout(Workout):
    id: int
    tags: List[DBTag]


@dataclass(kw_only=True)
class DBWorkoutStyle(DBWorkout):
    style: DBStyle
