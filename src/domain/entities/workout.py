from dataclasses import dataclass
from typing import List

from src.domain.entities.style import DBStyle
from src.domain.value_objects.workout import LevelsEnum
from src.application.tag.dto import ResponseWorkoutTagDTO


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
    tags: List[ResponseWorkoutTagDTO]


@dataclass(kw_only=True)
class DBWorkout(Workout):
    id: int


@dataclass(kw_only=True)
class DBWorkoutStyle(DBWorkout):
    style: DBStyle
