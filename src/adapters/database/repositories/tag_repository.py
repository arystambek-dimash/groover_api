from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.database.models import TagOrm
from src.domain.entities.style import DBStyle
from src.domain.entities.tag import DBTagWorkout, Tag, DBTag
from src.domain.entities.workout import DBWorkoutStyle
from src.domain.exceptions.base import NotFound


class TagRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, tag: Tag) -> DBTag:
        tag_orm = TagOrm(name=tag.name, usages=0)
        self._session.add(tag_orm)
        await self._session.flush()
        await self._session.refresh(tag_orm)
        return self._map_to_db_tag(tag_orm)

    async def get(self, item_id: int) -> Optional[DBTag]:
        stmt = select(TagOrm).where(TagOrm.id == item_id)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        if tag_orm:
            return self._map_to_db_tag(tag_orm)
        return None

    async def list(self) -> List[DBTag]:
        stmt = select(TagOrm)
        result = await self._session.execute(stmt)
        tag_orms = result.scalars().all()
        return [self._map_to_db_tag(tag_orm) for tag_orm in tag_orms]

    async def update(self, item: DBTag) -> None:
        stmt = select(TagOrm).where(TagOrm.id == item.id)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        tag_orm.name = item.name
        await self._session.flush()

    async def delete(self, item_id: int) -> None:
        stmt = select(TagOrm).where(TagOrm.id == item_id)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        await self._session.delete(tag_orm)
        await self._session.flush()

    async def increment_usages(self, tag_id: int) -> int:
        stmt = select(TagOrm).where(TagOrm.id == tag_id)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        if tag_orm.usages is None:
            tag_orm.usages = 1
        else:
            tag_orm.usages += 1
        await self._session.flush()
        await self._session.refresh(tag_orm)
        return tag_orm.usages

    async def decrement_usages(self, tag_id: int) -> int:
        stmt = select(TagOrm).where(TagOrm.id == tag_id)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        if not tag_orm:
            raise NotFound(f"Tag with id {tag_id} not found.")
        if tag_orm.usages and tag_orm.usages > 0:
            tag_orm.usages -= 1
        await self._session.flush()
        await self._session.refresh(tag_orm)
        return tag_orm.usages

    async def search_by_constraints(
            self,
            name: Optional[str] = None,
            min_usages: Optional[int] = None,
            max_usages: Optional[int] = None,
            with_workout: Optional[bool] = False
    ) -> List[DBTag]:
        stmt = select(TagOrm)
        if name:
            stmt = stmt.where(TagOrm.name.ilike(f"%{name}%"))
        if min_usages is not None:
            stmt = stmt.where(TagOrm.usages >= min_usages)
        if max_usages is not None:
            stmt = stmt.where(TagOrm.usages <= max_usages)
        if with_workout:
            stmt = stmt.options(selectinload(TagOrm.workouts))
        result = await self._session.execute(stmt)
        tag_orms = result.scalars().all()
        if with_workout:
            return [self._map_to_db_tag_workouts(tag_orm) for tag_orm in tag_orms]
        else:
            return [self._map_to_db_tag(tag_orm) for tag_orm in tag_orms]

    async def get_with_workouts(self, tag_id: int) -> Optional[DBTagWorkout]:
        stmt = (
            select(TagOrm)
            .where(TagOrm.id == tag_id)
            .options(
                selectinload(TagOrm.workouts).selectinload('style'),
                selectinload(TagOrm.workouts).selectinload('tags')
            )
        )
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        if tag_orm:
            return self._map_to_db_tag_workouts(tag_orm)
        return None

    async def get_by_name(self, name: str) -> Optional[DBTag]:
        stmt = select(TagOrm).where(TagOrm.name == name)
        result = await self._session.execute(stmt)
        tag_orm = result.scalar_one_or_none()
        if tag_orm:
            return self._map_to_db_tag(tag_orm)
        return None

    @staticmethod
    def _map_to_db_tag(tag: TagOrm) -> DBTag:
        return DBTag(
            id=tag.id,
            name=tag.name,
            usages=tag.usages
        )

    @staticmethod
    def _map_to_db_tag_workouts(tag: TagOrm) -> DBTagWorkout:
        return DBTagWorkout(
            id=tag.id,
            name=tag.name,
            usages=tag.usages,
            workouts=[
                DBWorkoutStyle(
                    id=db_workout.id,
                    name=db_workout.name,
                    calories=db_workout.calories,
                    duration=db_workout.duration,
                    level=db_workout.level,
                    description=db_workout.description,
                    dance_video=db_workout.dance_video,
                    thumbnail_image=db_workout.thumbnail_image,
                    author_name=db_workout.author_name,
                    views_count=db_workout.views_count,
                    style_id=db_workout.style_id,
                    style=DBStyle(
                        id=db_workout.style.id,
                        name=db_workout.style.name,
                        image_url=db_workout.style.image_url
                    ) if db_workout.style else None,
                    tags=[
                        DBTag(id=tag.id, name=tag.name)
                        for tag in db_workout.tags
                    ],
                )
                for db_workout in tag.workouts
            ]
        )
