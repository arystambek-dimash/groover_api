from dataclasses import dataclass
from src.domain.entities.user import DBUser


@dataclass
class Client:
    user: DBUser


@dataclass(kw_only=True)
class DBClient(Client):
    id: int
