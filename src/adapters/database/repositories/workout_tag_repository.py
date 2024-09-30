from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from sqlalchemy.dialects.postgresql import insert

from src.adapters.database.models import workout_tag_association_orm


class WorkoutTagAssociationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def insert_workout_tag_association(self, workout_id: int, tag_id: int):
        stmt = insert(workout_tag_association_orm).values(workout_id=workout_id, tag_id=tag_id)
        stmt = stmt.on_conflict_do_nothing(index_elements=['workout_id', 'tag_id'])

        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_workout_tag_association(self, workout_id: int, tag_id: int):
        stmt = delete(workout_tag_association_orm).where(
            workout_tag_association_orm.c.workout_id == workout_id,
            workout_tag_association_orm.c.tag_id == tag_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_workout_tag_association(self, workout_id: int, tag_id: int):
        stmt = select(workout_tag_association_orm).where(
            workout_tag_association_orm.c.workout_id == workout_id,
            workout_tag_association_orm.c.tag_id == tag_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_workout_id(self, workout_id: int):
        stmt = select(workout_tag_association_orm).where(
            workout_tag_association_orm.c.workout_id == workout_id
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
