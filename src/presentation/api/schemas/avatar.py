from pydantic import BaseModel


class AvatarBase(BaseModel):
    pass


class AvatarCreate(AvatarBase):
    pass


class AvatarUpdate(AvatarBase):
    pass


class Avatar(AvatarBase):
    id: int
    image_url: str | None

    class Config:
        from_attributes = True
