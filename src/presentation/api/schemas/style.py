from typing import Optional, List, Dict
from pydantic import BaseModel

from src.presentation.api.schemas.base import AsForm


class StyleCreate(AsForm):
    name: str


class StyleUpdate(AsForm):
    name: Optional[str] = None


class Style(BaseModel):
    id: int
    name: str
    image_url: str


class StyleWorkout(BaseModel):
    id: int
    name: str
    thumbnail_image: str
    author_name: str
    views_count: int


class StyleWithWorkouts(Style):
    workouts: List[StyleWorkout]

    class Config:
        populate_by_name = True
