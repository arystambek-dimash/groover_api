from dataclasses import asdict
from typing import List
from src.application.interfaces.repository import (
    WorkoutRepository,
    StyleRepository,
    TagRepository,
    WorkoutTagAssociationRepository,
)
from src.application.interfaces.uow import UoW
from src.application.workout.dto import (
    WorkoutCreateDTO,
    WorkoutUpdateDTO,
    WorkoutResponseStyleDTO,
    WorkoutResponseDTO, ViewsUpdateResponseDTO,
)
from src.domain.entities.workout import Workout
from src.domain.services.tag import TagService
from src.domain.services.upload import UploadService
from src.domain.services.workout import WorkoutService
from src.domain.exceptions.base import NotFound, AlreadyExists, InternalServerError, BadRequest


class WorkoutInteractor:
    def __init__(
            self,
            workout_repository: WorkoutRepository,
            style_repository: StyleRepository,
            tag_repository: TagRepository,
            workout_tag_association_repository: WorkoutTagAssociationRepository,
            uow: UoW,
            workout_service: WorkoutService,
            tag_service: TagService,
            upload_service: UploadService
    ):
        self._workout_repository = workout_repository
        self._style_repository = style_repository
        self._tag_repository = tag_repository
        self._workout_tag_association_repository = workout_tag_association_repository
        self._uow = uow
        self._workout_service = workout_service
        self._tag_service = tag_service
        self._upload_service = upload_service

    async def create_workout(self, dto: WorkoutCreateDTO) -> WorkoutResponseStyleDTO:
        async with self._uow:
            image_url = None
            existing_workout = await self._workout_repository.get_by_name(dto.name)
            if existing_workout:
                raise AlreadyExists(f"Workout with name '{dto.name}' already exists.")

            db_style = await self._style_repository.get(dto.style_id)
            if not db_style:
                raise NotFound(f"Style with id {dto.style_id} not found.")

            try:
                image_url = await self._upload_service.upload_file(
                    file=dto.thumbnail_image.file,
                    filename=dto.thumbnail_image.filename,
                    file_dir=dto.thumbnail_image.filedir
                )
                dto.thumbnail_image = image_url.url

                workout_entity: Workout = self._workout_service.create_workout_entity(dto)
                created_workout = await self._workout_repository.add(workout_entity)
                await self._handle_tags_for_workout(created_workout.id, dto.tags or [])

                await self._uow.commit()

            except Exception as e:
                await self._uow.rollback()
                if image_url:
                    await self._upload_service.delete_file(image_url.url)
                raise e
        return self._map_to_response_dto(created_workout)

    async def get_workout(self, workout_id: int) -> WorkoutResponseStyleDTO:
        workout = await self._workout_repository.get(workout_id)
        if not workout:
            raise NotFound(f"Workout with id {workout_id} not found.")
        return self._map_to_response_style_dto(workout)

    async def list_workouts(self) -> List[WorkoutResponseStyleDTO]:
        workouts = await self._workout_repository.list()
        return [self._map_to_response_style_dto(workout) for workout in workouts]

    async def add_tag_for_workout(self, workout_id: int, tags: List[str]) -> bool:
        async with self._uow:
            existing_workout = await self._workout_repository.get(workout_id)
            if not existing_workout:
                raise NotFound(f"Workout with id {workout_id} not found.")

            await self._handle_tags_for_workout(workout_id, tags)

            await self._uow.commit()
            return True

    async def delete_tag_from_workout(self, workout_id: int, tag_id: int) -> WorkoutResponseDTO:
        async with self._uow:
            existing_workout = await self._workout_repository.get(workout_id)
            if not existing_workout:
                raise NotFound(f"Workout with id {workout_id} not found.")

            existing_tag = await self._tag_repository.get(tag_id)
            if not existing_tag:
                raise NotFound(f"Tag with id {tag_id} not found.")

            has_association = await self._workout_tag_association_repository.get_workout_tag_association(
                workout_id, tag_id
            )
            if not has_association:
                raise BadRequest('No association between tag and workout')

            await self._workout_tag_association_repository.delete_workout_tag_association(
                workout_id, tag_id
            )
            await self._tag_repository.decrement_usages(tag_id)
            await self._uow.commit()

            return True

    async def update_workout(self, workout_id: int, dto: WorkoutUpdateDTO) -> WorkoutResponseStyleDTO:
        async with self._uow:
            image_url = None
            try:
                existing_workout = await self._workout_repository.get(workout_id)
                if not existing_workout:
                    raise NotFound(f"Workout with id {workout_id} not found.")
                if dto.name:
                    existing_by_name = await self._workout_repository.get_by_name(dto.name)
                    if existing_by_name and existing_by_name.id != workout_id:
                        raise AlreadyExists(f"Workout with name '{dto.name}' already exists.")
                if dto.style_id:
                    existing_style = await self._style_repository.get(dto.style_id)
                    if not existing_style:
                        raise NotFound(f"Style with id {dto.style_id} not found.")
                if dto.thumbnail_image:
                    image_url = await self._upload_service.upload_file(
                        file=dto.thumbnail_image.file,
                        filename=dto.thumbnail_image.filename,
                        file_dir=dto.thumbnail_image.filedir
                    )
                    dto.thumbnail_image = image_url.url
                    if existing_workout.thumbnail_image:
                        await self._upload_service.delete_file(existing_workout.thumbnail_image)
                else:
                    dto.thumbnail_image = None

                updated_entity = self._workout_service.update_workout(existing_workout, dto)
                updated_workout = await self._workout_repository.update(updated_entity)
                await self._uow.commit()

                return self._map_to_response_style_dto(updated_workout)

            except Exception as e:
                await self._uow.rollback()
                if image_url:
                    await self._upload_service.delete_file(image_url.url)
                raise e

    async def update_workout_views(self, workout_id: int) -> ViewsUpdateResponseDTO:
        async with self._uow:
            try:
                existing_workout = await self._workout_repository.get(workout_id)
                if not existing_workout:
                    raise NotFound(f"Workout with id {workout_id} not found.")
                updated_view_workout = await self._workout_repository.update_workout_views(workout_id)
                return ViewsUpdateResponseDTO(id=updated_view_workout.id, views_count=updated_view_workout.views_count)
            except Exception as e:
                await self._uow.rollback()
                raise e

    async def delete_workout(self, workout_id: int) -> None:
        async with self._uow:
            workout = await self._workout_repository.get(workout_id)
            if not workout:
                raise NotFound(f"Workout with id {workout_id} not found.")

            tag_ids = await self._workout_tag_association_repository.get_by_workout_id(workout_id)
            for tag_id in tag_ids:
                await self._workout_tag_association_repository.delete_workout_tag_association(
                    workout_id, tag_id
                )
                await self._tag_repository.decrement_usages(tag_id)

            await self._workout_repository.delete(workout_id)
            await self._uow.commit()

    async def _handle_tags_for_workout(self, workout_id: int, tags: List[str]):
        for tag_name in tags:
            existing_tag = await self._tag_repository.get_by_name(tag_name)
            if not existing_tag:
                new_tag = self._tag_service.create_tag_entity(tag_name)
                db_tag = await self._tag_repository.add(new_tag)
                tag_id = db_tag.id
            else:
                tag_id = existing_tag.id
            has_association = await self._workout_tag_association_repository.get_workout_tag_association(
                workout_id, tag_id
            )
            if not has_association:
                await self._workout_tag_association_repository.insert_workout_tag_association(
                    workout_id=workout_id, tag_id=tag_id
                )
                await self._tag_repository.increment_usages(tag_id)

    @staticmethod
    def _map_to_response_style_dto(workout: Workout) -> WorkoutResponseStyleDTO:
        return WorkoutResponseStyleDTO(**asdict(workout))

    @staticmethod
    def _map_to_response_dto(workout: Workout) -> WorkoutResponseDTO:
        return WorkoutResponseDTO(**asdict(workout))
