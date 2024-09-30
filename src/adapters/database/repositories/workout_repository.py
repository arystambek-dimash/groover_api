from dataclasses import asdict
from typing import List, Optional, Union
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.adapters.database.models import WorkoutOrm
from src.domain.entities.style import DBStyle
from src.domain.entities.workout import DBWorkout, Workout, DBWorkoutStyle
from src.domain.entities.tag import DBTag


class WorkoutRepositoryImpl:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self._session = session

    async def add(self, workout: Workout) -> DBWorkout:
        workout_data = asdict(workout)
        workout_data.pop("tags", None)

        stmt = insert(WorkoutOrm).values(**workout_data).returning(WorkoutOrm).options(
            selectinload(WorkoutOrm.tags)
        )
        result = await self._session.execute(stmt)
        workout = result.scalar_one()
        await self._session.flush()
        return self._map_to_db_workout(workout, False)

    async def get(self, workout_id: int) -> Optional[DBWorkout]:
        stmt = select(WorkoutOrm).where(WorkoutOrm.id == workout_id).options(
            selectinload(WorkoutOrm.tags),
            selectinload(WorkoutOrm.style)
        )
        result = await self._session.execute(stmt)
        workout_orm = result.scalar_one_or_none()
        return self._map_to_db_workout(workout_orm, True) if workout_orm else None

    async def get_by_name(self, workout_name: str) -> Optional[
        DBWorkout]:
        stmt = select(WorkoutOrm).where(WorkoutOrm.name == workout_name).options(
            selectinload(WorkoutOrm.tags),
            selectinload(WorkoutOrm.style)
        )
        result = await self._session.execute(stmt)
        workout_orm = result.scalar_one_or_none()
        return self._map_to_db_workout(workout_orm, True) if workout_orm else None

    async def list(self) -> List[DBWorkout]:
        stmt = select(WorkoutOrm).options(
            selectinload(WorkoutOrm.tags),
            selectinload(WorkoutOrm.style)
        )
        result = await self._session.execute(stmt)
        workout_orms = result.scalars().all()
        return [self._map_to_db_workout(w, True) for w in workout_orms]

    async def update(self, workout: DBWorkout) -> DBWorkout:
        workout_data = asdict(workout)
        workout_data.pop('tags', None)
        stmt = (
            update(WorkoutOrm)
            .where(WorkoutOrm.id == workout.id)
            .values(**workout_data)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.flush()

        result = await self._session.execute(
            select(WorkoutOrm)
            .where(WorkoutOrm.id == workout.id)
            .options(selectinload(WorkoutOrm.tags))
            .options(selectinload(WorkoutOrm.style))
        )
        db_workout = result.scalar_one()

        return self._map_to_db_workout(db_workout, True)

    async def delete(self, workout_id: int) -> None:
        stmt = delete(WorkoutOrm).where(WorkoutOrm.id == workout_id)
        await self._session.execute(stmt)
        await self._session.flush()

    @staticmethod
    def _map_to_db_workout(workout_orm: WorkoutOrm, with_style: bool) -> Union[DBWorkout, DBWorkoutStyle]:
        base_kwargs = {
            'id': workout_orm.id,
            'name': workout_orm.name,
            'calories': workout_orm.calories,
            'duration': workout_orm.duration,
            'level': workout_orm.level,
            'description': workout_orm.description,
            'dance_video': workout_orm.dance_video,
            'thumbnail_image': workout_orm.thumbnail_image,
            'author_name': workout_orm.author_name,
            'views_count': workout_orm.views_count,
            'style_id': workout_orm.style_id,
            'tags': [DBTag(id=tag.id, name=tag.name, usages=tag.usages) for tag in workout_orm.tags],
        }

        if with_style and workout_orm.style:
            base_kwargs['style'] = DBStyle(
                id=workout_orm.style.id,
                name=workout_orm.style.name,
                image_url=workout_orm.style.image_url
            )
            return DBWorkoutStyle(**base_kwargs)
        else:
            return DBWorkout(**base_kwargs)
