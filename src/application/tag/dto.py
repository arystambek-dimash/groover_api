from dataclasses import dataclass
from typing import Optional, List

from src.domain.entities.pagination import PaginatedResponseDTO


@dataclass
class CreateTagDTO:
    name: str


@dataclass
class ResponseTagDTO:
    id: int
    name: str
    usages: int


@dataclass
class ResponseRecommendationTagDTO:
    tags: PaginatedResponseDTO[ResponseTagDTO]
    popular: PaginatedResponseDTO[ResponseTagDTO]


@dataclass
class ResponseWorkoutTagDTO:
    id: int
    name: str


@dataclass
class ResponseTagWorkoutDTO(ResponseTagDTO):
    workouts: List['WorkoutResponseDTO']


@dataclass
class UpdateTagDTO:
    name: Optional[str] = None
