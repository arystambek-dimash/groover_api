from dataclasses import dataclass
from typing import Optional

from src.domain.entities.upload import CreateUpload


@dataclass(kw_only=True)
class CreateAvatarDTO:
    upload: CreateUpload


@dataclass(kw_only=True)
class UpdateAvatarDTO:
    upload: Optional[CreateUpload] = None


@dataclass(kw_only=True)
class ResponseAvatarDTO:
    id: int
    image_url: str
