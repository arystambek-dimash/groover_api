from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union

from src.presentation.api.schemas.base import AsForm
from src.presentation.api.schemas.style import Style
from src.presentation.api.schemas.tag import Tag

from src.adapters.database.models.workout import LevelsEnum


class Workout(BaseModel):
    id: Optional[int]
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: str
    author_name: str
    views_count: int
    tags: List[Tag]

    class Config:
        from_attributes = True


class WorkoutStyle(Workout):
    style: Style


class WorkoutCreate(AsForm):
    name: str = Field(...)
    calories: int = Field(...)
    duration: int = Field(...)
    level: LevelsEnum = Field(...)
    description: str = Field(...)
    dance_video: str = Field(...)
    author_name: str = Field(...)
    style_id: int = Field(...)
    tags: List[str]

    class Config:
        from_attributes = True


class WorkoutUpdate(AsForm):
    name: Optional[str] = None
    calories: Optional[int] = None
    duration: Optional[int] = None
    level: Optional[LevelsEnum] = None
    description: Optional[str] = None
    dance_video: Optional[str] = None
    author_name: Optional[str] = None
    style_id: Optional[Union[int, str]] = None

    @validator('calories', 'duration', 'style_id', pre=True, always=True)
    def empty_str_to_none(cls, v):
        return None if v == '' else v

    class Config:
        from_attributes = True


class WorkoutList(BaseModel):
    workouts: List[Workout]

    class Config:
        from_attribute = True
