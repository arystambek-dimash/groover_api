from typing import Optional, Union

from pydantic import BaseModel

from src.domain.value_objects.staff import StaffRole


class UserSchema(BaseModel):
    email: str
    password: str


class UpdateUserSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    avatar_id: Optional[int] = None


class StaffSchema(BaseModel):
    email: str
    password: str
    role: StaffRole


class ResponseUserSchema(BaseModel):
    id: int
    email: str
    username: str
    avatar_url: Union[str, None]
    is_staff: bool = False
    is_manager: bool = False
    role: Optional[str] = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    role: str = 'CLIENT'
