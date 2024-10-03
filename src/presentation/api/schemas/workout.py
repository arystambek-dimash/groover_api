from pydantic import BaseModel, Field, validator
from typing import List, Optional, Union

from src.presentation.api.schemas.base import AsForm

from src.adapters.database.models.workout import LevelsEnum


class WorkoutTag(BaseModel):
    id: int
    name: str


class Workout(BaseModel):
    id: Optional[int]
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: str
    tags: List[WorkoutTag]

    class Config:
        from_attributes = True
        populate_by_name = True


class WorkoutViewResponse(BaseModel):
    id: int
    views_count: int


class WorkoutStyle(BaseModel):
    id: int
    name: str
    image_url: str


class WorkoutWithStyle(Workout):
    style: WorkoutStyle

    class Config:
        from_attributes = True


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
    calories: Union[Optional[int], Optional[str]] = None
    duration: Union[Optional[int], Optional[str]] = None
    level: Union[Optional[LevelsEnum], Optional[str]] = None
    description: Optional[str] = None
    dance_video: Optional[str] = None
    author_name: Optional[str] = None

    @validator('calories', 'duration', pre=True, always=True)
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == '':
            return None
        return v

    class Config:
        from_attributes = True


class WorkoutList(BaseModel):
    workouts: List[Workout]

    class Config:
        from_attributes = True
