from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Tag:
    name: str


@dataclass(frozen=True)
class DBTag(Tag):
    id: int
    workouts: List['Workout']
