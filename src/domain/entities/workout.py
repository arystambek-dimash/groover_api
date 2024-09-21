from dataclasses import dataclass
from typing import List

from src.adapters.database.models.workout import LevelsEnum


@dataclass
class Workout:
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: str
    instructor_name: str
    views_count: int
    style_id: int


@dataclass
class DBWorkout:
    id: int
    tags: List['Tag']
    style: 'Style'
