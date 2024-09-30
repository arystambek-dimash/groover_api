import sqlalchemy as sa

from src.adapters.database.config import Base

workout_tag_association_orm = sa.Table(
    'workout_tag_association',
    Base.metadata,
    sa.Column('workout_id', sa.ForeignKey('workouts.id', ondelete="CASCADE"), primary_key=True),
    sa.Column('tag_id', sa.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True),
    sa.PrimaryKeyConstraint('workout_id', 'tag_id', name='pk_workout_tag_association')
)
