import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database.config import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(
        sa.String, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    avatar_id: Mapped[int] = mapped_column(
        sa.ForeignKey('avatars.id', ondelete='SET NULL'), nullable=True
    )
    client = relationship('ClientOrm', lazy='selectin', back_populates="user", uselist=False)
    staff = relationship('StaffOrm', lazy='joined', back_populates="user", uselist=False)

    avatar = relationship('AvatarOrm', back_populates="users", uselist=False)
