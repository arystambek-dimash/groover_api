from typing import Optional, List, Mapping

from pydantic import BaseModel

from src.domain.entities.workout import Workout
from src.presentation.api.schemas.base import AsForm


class StyleCreate(AsForm):
    name: str


class StyleUpdate(AsForm):
    name: Optional[str] = None


class Style(BaseModel):
    id: int
    name: str
    image_url: str


class StyleWithWorkouts(Style):
    workouts: List[Workout]
