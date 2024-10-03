from dataclasses import dataclass
from typing import Optional, List

from src.domain.entities.upload import CreateUpload


@dataclass
class CreateStyleDTO:
    name: str
    image_file: CreateUpload


@dataclass
class ResponseStyleDTO:
    id: int
    name: str
    image_url: str


@dataclass
class ResponseStyleWorkoutsDTO:
    id: int
    name: str
    image_url: str
    workouts: List['WorkoutResponseDTO']


@dataclass
class UpdateStyleDTO:
    name: Optional[str] = None
    image_file: Optional[CreateUpload] = None
