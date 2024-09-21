import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database.config import Base


class ClientOrm(Base):
    __tablename__ = 'auth_clients'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = relationship('UserOrm', back_populates='client', uselist=False)
