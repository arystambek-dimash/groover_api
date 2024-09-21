from dataclasses import dataclass

from src.domain.entities.user import DBUser
from src.domain.value_objects.staff import StaffRole


@dataclass
class Staff:
    user: DBUser
    role: StaffRole


@dataclass(kw_only=True)
class DBStaff(Staff):
    id: int
