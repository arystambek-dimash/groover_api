from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.database.models import StyleOrm, WorkoutOrm
from src.domain.entities.style import DBStyle, DBStyleWorkout, Style
from src.domain.entities.tag import DBTag
from src.domain.entities.workout import DBWorkout


class StyleRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, item: Style) -> DBStyle:
        style_orm = StyleOrm(
            name=item.name,
            image_url=str(item.image_url)
        )
        self.session.add(style_orm)
        await self.session.flush()
        await self.session.refresh(style_orm)
        return self._map_to_db_style(style_orm)

    async def get(self, item_id: int) -> Optional[DBStyle]:
        stmt = select(StyleOrm).where(StyleOrm.id == item_id)
        result = await self.session.execute(stmt)
        style_orm = result.scalar_one_or_none()
        if style_orm:
            return self._map_to_db_style(style_orm)
        else:
            return None

    async def list(self) -> List[DBStyle]:
        stmt = select(StyleOrm)
        result = await self.session.execute(stmt)
        style_orms = result.scalars().all()
        return [self._map_to_db_style(style_orm) for style_orm in style_orms]

    async def update(self, item: DBStyle) -> None:
        stmt = select(StyleOrm).where(StyleOrm.id == item.id)
        result = await self.session.execute(stmt)
        style_orm = result.scalar_one_or_none()
        style_orm.name = item.name
        style_orm.image_url = str(item.image_url)
        await self.session.flush()

    async def delete(self, item_id: int) -> None:
        stmt = delete(StyleOrm).where(StyleOrm.id == item_id)
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_with_workouts(self, style_id: int) -> Optional[DBStyleWorkout]:
        stmt = (
            select(StyleOrm)
            .where(StyleOrm.id == style_id)
            .options(selectinload(StyleOrm.workouts).options(selectinload(WorkoutOrm.tags)))
        )
        result = await self.session.execute(stmt)
        style_orm = result.scalar_one_or_none()
        if style_orm:
            return self._map_to_db_style_workouts(style_orm)
        else:
            return None

    async def get_by_name(self, name: str) -> Optional[DBStyle]:
        stmt = select(StyleOrm).where(StyleOrm.name == name)
        result = await self.session.execute(stmt)
        style_orm = result.scalar_one_or_none()
        if style_orm:
            return self._map_to_db_style(style_orm)
        else:
            return None

    @staticmethod
    def _map_to_db_style(style: StyleOrm) -> DBStyle:
        return DBStyle(
            id=style.id,
            name=style.name,
            image_url=style.image_url
        )

    @staticmethod
    def _map_to_db_style_workouts(style: StyleOrm) -> DBStyleWorkout:
        return DBStyleWorkout(
            id=style.id,
            name=style.name,
            image_url=style.image_url,
            workouts=[DBWorkout(id=workout_orm.id,
                                name=workout_orm.name,
                                calories=workout_orm.calories,
                                duration=workout_orm.duration,
                                level=workout_orm.level,
                                description=workout_orm.description,
                                dance_video=workout_orm.dance_video,
                                thumbnail_image=workout_orm.thumbnail_image,
                                author_name=workout_orm.author_name,
                                views_count=workout_orm.views_count,
                                style_id=workout_orm.style_id,
                                tags=[
                                    DBTag(id=tag.id, name=tag.name)
                                    for tag in workout_orm.tags],
                                ) for workout_orm in style.workouts]
        )
