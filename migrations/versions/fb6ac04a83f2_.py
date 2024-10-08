"""empty message

Revision ID: fb6ac04a83f2
Revises: 
Create Date: 2024-09-20 23:29:24.322794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb6ac04a83f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('styles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('profile_image', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('auth_clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'MANAGER', name='staffrole'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('calories', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('level', sa.Enum('BEGINNER', 'INTERMEDIATE', 'IMPOSSIBLE', name='levelsenum'), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('dance_video', sa.String(), nullable=False),
    sa.Column('thumbnail_image', sa.String(), nullable=False),
    sa.Column('instructor_name', sa.String(), nullable=False),
    sa.Column('views_count', sa.Integer(), nullable=False),
    sa.Column('style_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['style_id'], ['styles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workouts_name'), 'workouts', ['name'], unique=False)
    op.create_table('workout_tag_association',
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('workout_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workout_tag_association')
    op.drop_index(op.f('ix_workouts_name'), table_name='workouts')
    op.drop_table('workouts')
    op.drop_table('staffs')
    op.drop_table('auth_clients')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('tags')
    op.drop_table('styles')
    # ### end Alembic commands ###
