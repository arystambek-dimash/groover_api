from pydantic import BaseModel
from typing import Optional, List

from src.domain.entities.workout import DBWorkout


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: Optional[str] = None


class Tag(BaseModel):
    id: int
    name: str
    usages: int | None


class TagWorkouts(Tag):
    workouts: List[DBWorkout]


class TagList(BaseModel):
    tags: List[Tag]
