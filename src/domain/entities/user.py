from dataclasses import dataclass, field
import uuid

from src.domain.value_objects.user import UserEmail, UserPassword


def generate_username():
    return f"user_{uuid.uuid4().hex[:8]}"


@dataclass
class User:
    email: UserEmail
    password: UserPassword
    avatar_id: int
    username: str = field(default_factory=generate_username)

    def __post_init__(self):
        pass


@dataclass(kw_only=True)
class DBUser(User):
    id: int
    avatar_url: str
    role: str = 'CLIENT'
