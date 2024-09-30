from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import  DBWorkout


@dataclass
class Style:
    name: str
    image_url: str


@dataclass(kw_only=True)
class DBStyle(Style):
    id: int


@dataclass(kw_only=True)
class DBStyleWorkout(DBStyle):
    workouts: List['DBWorkout']
