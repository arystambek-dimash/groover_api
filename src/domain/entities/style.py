from dataclasses import dataclass
from typing import List


@dataclass
class Style:
    name: str
    image_url: str


@dataclass
class DBStyle:
    id: int
    workouts: List['Workout']
