from enum import Enum as PyEnum
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.database.config import Base
from .workout_to_tags import workout_tag_association_orm


class LevelsEnum(PyEnum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    IMPOSSIBLE = 'impossible'


class WorkoutOrm(Base):
    __tablename__ = 'workouts'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, index=True)
    calories: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    duration: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    level: Mapped[LevelsEnum] = mapped_column(sa.Enum(LevelsEnum), nullable=False)
    description: Mapped[str] = mapped_column(sa.String, nullable=False)
    dance_video: Mapped[str] = mapped_column(sa.String, nullable=False)
    thumbnail_image: Mapped[str] = mapped_column(sa.String, nullable=False)
    instructor_name: Mapped[str] = mapped_column(sa.String, nullable=False)
    views_count: Mapped[int] = mapped_column(sa.Integer, default=0)

    tags = relationship('TagOrm', secondary=workout_tag_association_orm, back_populates='workouts')
    style_id: Mapped[int] = mapped_column(sa.ForeignKey('styles.id'), nullable=False)
    style = relationship('StyleOrm', back_populates='workouts')
