from dataclasses import dataclass


@dataclass
class Avatar:
    image_url: str


@dataclass(kw_only=True)
class DBAvatar(Avatar):
    id: int
