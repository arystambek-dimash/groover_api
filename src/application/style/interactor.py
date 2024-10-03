from typing import List, Union
from src.application.interfaces.uow import UoW
from src.application.interfaces.repository import StyleRepository
from src.application.style.dto import CreateStyleDTO, UpdateStyleDTO, ResponseStyleWorkoutsDTO, ResponseStyleDTO
from src.application.tag.dto import ResponseWorkoutTagDTO
from src.application.workout.dto import WorkoutResponseDTO
from src.domain.entities.tag import DBTag
from src.domain.entities.style import DBStyle, DBStyleWorkout
from src.domain.exceptions.base import DataConflict, NotFound
from src.domain.services.style import StyleService
from src.domain.services.upload import UploadService


class StyleInteractor:
    def __init__(self,
                 style_repository: StyleRepository,
                 uow: UoW,
                 style_service: StyleService,
                 upload_service: UploadService):
        self.style_repository = style_repository
        self.uow = uow
        self.style_service = style_service
        self._upload_service = upload_service

    async def create_style(self, dto: CreateStyleDTO) -> ResponseStyleDTO:
        async with self.uow:
            image_url = None
            try:
                existing_style = await self.style_repository.get_by_name(dto.name)
                if existing_style:
                    raise DataConflict(f"Style with name '{dto.name}' already exists.")
                image_url = await self._upload_service.upload_file(dto.image_file.file,
                                                                   dto.image_file.filename,
                                                                   dto.image_file.filedir)
                style_entity = await self.style_service.create_style(dto.name, image_url.url)
                db_style: DBStyle = await self.style_repository.add(style_entity)
                await self.uow.commit()
                return ResponseStyleDTO(
                    id=db_style.id,
                    name=db_style.name,
                    image_url=db_style.image_url
                )
            except Exception as e:
                if image_url is not None:
                    await self._upload_service.delete_file(image_url.url)
                await self.uow.rollback()
                raise e

    async def get_style(self, style_id: int, with_workouts: bool = False) -> Union[
        ResponseStyleDTO, ResponseStyleWorkoutsDTO]:
        if with_workouts:
            style = await self.style_repository.get_with_workouts(style_id)
        else:
            style = await self.style_repository.get(style_id)
        if not style:
            raise NotFound(f"Style with id {style_id} not found.")
        return self._map_to_response_entity(style, with_workouts)

    async def list_styles(self) -> List[ResponseStyleDTO]:
        styles = await self.style_repository.list()
        return [ResponseStyleDTO(id=style.id, name=style.name, image_url=style.image_url) for style in styles]

    async def update_style(self, style_id: int, dto: UpdateStyleDTO) -> ResponseStyleDTO:
        async with self.uow:
            db_style = await self.style_repository.get(style_id)
            if not db_style:
                raise NotFound(f"Style with id {style_id} not found.")

            if dto.name:
                existing_style = await self.style_repository.get_by_name(dto.name)
                if existing_style and existing_style.id != style_id:
                    raise DataConflict(f"Style with name '{dto.name}' already exists.")

            image_url = db_style.image_url
            if dto.image_file:
                image_url_obj = await self._upload_service.upload_file(
                    dto.image_file.file,
                    dto.image_file.filename,
                    dto.image_file.filedir
                )
                image_url = image_url_obj.url

            updated_style = await self.style_service.update_style(
                db_style=db_style,
                name=dto.name if dto.name else db_style.name,
                image_url=image_url
            )
            await self.style_repository.update(updated_style)
            await self.uow.commit()
            return ResponseStyleDTO(
                id=updated_style.id,
                name=updated_style.name,
                image_url=updated_style.image_url
            )

    async def delete_style(self, style_id: int) -> None:
        async with self.uow:
            style = await self.style_repository.get(style_id)
            if not style:
                raise NotFound(f"Style with id {style_id} not found.")
            await self.style_repository.delete(style_id)
            await self.uow.commit()

    @staticmethod
    def _map_to_response_entity(entity: Union[DBStyle, DBStyleWorkout], with_workouts: bool = False) -> Union[
        ResponseStyleWorkoutsDTO, ResponseStyleDTO]:
        if with_workouts:
            return ResponseStyleWorkoutsDTO(
                id=entity.id,
                name=entity.name,
                image_url=entity.image_url,
                workouts=[
                    WorkoutResponseDTO(
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
                        tags=[ResponseWorkoutTagDTO(id=tag.id, name=tag.name) for tag in db_workout.tags],
                    ) for db_workout in entity.workouts
                ]
            )
        else:
            return ResponseStyleDTO(
                id=entity.id,
                name=entity.name,
                image_url=entity.image_url
            )
