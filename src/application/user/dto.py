from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects.staff import StaffRole


@dataclass(frozen=True)
class CreateUserDTO:
    email: str
    password: str


@dataclass(frozen=True)
class UserDTO:
    email: str
    password: str
    username: str
    profile_image: Optional[str]
    is_active: bool


@dataclass(frozen=True, kw_only=True)
class DBUserDTO(UserDTO):
    id: int


@dataclass(frozen=True)
class ResponseUserDTO:
    id: int
    email: str
    username: str
    profile_image: Optional[str]
    is_staff: bool = False
    role: Optional[str] = None


@dataclass(frozen=True)
class UserLoginDTO:
    email: str
    password: str


@dataclass
class TokenDTO:
    access_token: str
    refresh_token: str
    role: str = 'CLIENT'


@dataclass(frozen=True)
class UpdateUserDTO:
    password: Optional[str] = None
    username: Optional[str] = None
    profile_image: Optional[str] = None


@dataclass(frozen=True)
class CreateStaffDTO:
    email: str
    password: str
    role: StaffRole


@dataclass
class PayloadDTO:
    sub: int
    exp: int
