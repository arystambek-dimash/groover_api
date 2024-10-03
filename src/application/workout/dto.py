from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING, Union

from src.adapters.database.models.workout import LevelsEnum
from src.application.style.dto import ResponseStyleDTO
from src.domain.entities.upload import CreateUpload


@dataclass
class WorkoutResponseDTO:
    id: int
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: str
    author_name: str
    style_id: int
    views_count: int
    tags: List['ResponseWorkoutTagDTO']


@dataclass
class WorkoutResponseStyleDTO:
    id: int
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
    style: ResponseStyleDTO
    tags: List['ResponseWorkoutTagDTO']


@dataclass
class ViewsUpdateResponseDTO:
    id: int
    views_count: int


@dataclass
class WorkoutCreateDTO:
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    dance_video: str
    thumbnail_image: CreateUpload | str
    author_name: str
    style_id: int
    tags: Optional[List[str]]


@dataclass
class WorkoutUpdateDTO:
    name: Optional[str] = None
    calories: Optional[int] = None
    duration: Optional[int] = None
    level: Union[Optional[LevelsEnum], Optional[str]] = None
    description: Optional[str] = None
    dance_video: Optional[str] = None
    thumbnail_image: Optional[CreateUpload] | Optional[str] = None
    author_name: Optional[str] = None
