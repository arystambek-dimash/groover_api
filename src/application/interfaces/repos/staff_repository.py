from abc import ABC, abstractmethod
from src.domain.entities.staff import Staff, DBStaff


class StaffRepository(ABC):
    @abstractmethod
    async def create(self, staff: Staff) -> DBStaff:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> DBStaff | None:
        pass
