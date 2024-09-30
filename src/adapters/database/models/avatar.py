import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database.config import Base


class AvatarOrm(Base):
    __tablename__ = 'avatars'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    image_url: Mapped[str] = mapped_column(sa.String, nullable=True)

    users = relationship("UserOrm", back_populates="avatar")
