from dataclasses import dataclass
from typing import List, Optional

from src.adapters.database.models.workout import LevelsEnum
from src.application.tag.dto import ResponseTagDTO
from src.domain.entities.upload import CreateUpload


@dataclass
class WorkoutResponseDTO:
    id: int
    name: str
    calories: int
    duration: int
    level: LevelsEnum
    description: str
    style_id: int
    dance_video: str
    thumbnail_image: str
    author_name: str
    views_count: int
    tags: List[ResponseTagDTO]


@dataclass
class WorkoutResponseStyleDTO:
    from src.application.style.dto import ResponseStyleDTO
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
    tags: List[ResponseTagDTO]


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
    level: Optional[LevelsEnum] = None
    description: Optional[str] = None
    dance_video: Optional[str] = None
    thumbnail_image: Optional[CreateUpload] | Optional[str] = None
    author_name: Optional[str] = None
    style_id: Optional[int] = None
