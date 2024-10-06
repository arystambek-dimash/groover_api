from dataclasses import dataclass
from typing import TypeVar, Generic, List

T = TypeVar('T')


@dataclass
class PaginatedResponseDTO(Generic[T]):
    items: List[T]
    total_count: int
    page: int
    page_size: int
