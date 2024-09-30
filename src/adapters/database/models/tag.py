import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.adapters.database.config import Base

from .workout_to_tags import workout_tag_association_orm


class TagOrm(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    usages: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=True)
    workouts = relationship('WorkoutOrm', secondary=workout_tag_association_orm, back_populates='tags')
