import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.database.config import Base


class StyleOrm(Base):
    __tablename__ = 'styles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    image_url: Mapped[str] = mapped_column(sa.String, nullable=True)

    workouts = relationship('WorkoutOrm', back_populates='style')
