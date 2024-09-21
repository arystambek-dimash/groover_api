from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.domain.value_objects.staff import StaffRole


class UserSchema(BaseModel):
    email: str
    password: str


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    profile_image: Optional[str] = None
    password: Optional[str] = None


class StaffSchema(BaseModel):
    email: str
    password: str
    role: StaffRole


class ResponseUserSchema(BaseModel):
    id: int
    email: str
    username: str
    profile_image: Optional[str] = None
    is_staff: bool = False
    role: Optional[str] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    role: str = 'CLIENT'
