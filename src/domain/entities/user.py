from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
import uuid

from src.domain.value_objects.user import UserEmail, UserPassword


def generate_username():
    return f"user_{uuid.uuid4().hex[:8]}"


@dataclass
class User:
    email: UserEmail
    password: UserPassword
    username: str = field(default_factory=generate_username)
    profile_image: Optional[str] = None

    def __post_init__(self):
        pass


@dataclass(kw_only=True)
class DBUser(User):
    id: int
