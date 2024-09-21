from enum import Enum as PyEnum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database.config import Base
from src.domain.value_objects.staff import StaffRole


class StaffOrm(Base):
    __tablename__ = 'staffs'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role: Mapped[StaffRole] = mapped_column(sa.Enum(StaffRole, name='staffrole', create_type=False), nullable=False)

    user = relationship('UserOrm', back_populates='staff', uselist=False)
