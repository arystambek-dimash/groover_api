from pydantic import BaseModel
from typing import Optional, List


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: Optional[str] = None


class Tag(BaseModel):
    id: int
    name: str
    usages: int | None


class TagWorkout(BaseModel):
    id: int
    name: str
    thumbnail_image: str
    author_name: str
    views_count: int


class TagWorkouts(Tag):
    workouts: List[TagWorkout]


class PaginatedTag(BaseModel):
    items: List[Tag]
    total_count: int
    page: int
    page_size: int


class TagList(BaseModel):
    tags: List[Tag]
