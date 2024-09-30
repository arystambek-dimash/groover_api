from dataclasses import asdict
from typing import List, Union, Optional
from src.application.interfaces.repository import TagRepository
from src.application.interfaces.uow import UoW
from src.application.tag.dto import CreateTagDTO, UpdateTagDTO, ResponseTagDTO, ResponseTagWorkoutDTO
from src.domain.entities.tag import DBTag
from src.domain.exceptions.base import NotFound, AlreadyExists
from src.domain.services.tag import TagService


class TagInteractor:
    def __init__(
            self,
            tag_repository: TagRepository,
            uow: UoW,
            tag_service: TagService,
    ):
        self._tag_repository = tag_repository
        self._uow = uow
        self._tag_service = tag_service

    async def create_tag(self, tag_dto: CreateTagDTO) -> ResponseTagDTO:
        async with self._uow:
            existing_tag = await self._tag_repository.get_by_name(tag_dto.name)
            if existing_tag:
                raise AlreadyExists('Tag with such name already exists')
            tag = self._tag_service.create_tag_entity(tag_dto)
            db_tag: DBTag = await self._tag_repository.add(tag)
            await self._uow.commit()
            return ResponseTagDTO(**asdict(db_tag))

    async def get_tag(self, tag_id: int, with_workout: bool = False) -> ResponseTagDTO:
        if with_workout:
            tag = await self._tag_repository.get_with_workouts(tag_id)
        else:
            tag = await self._tag_repository.get(tag_id)
        if not tag:
            raise NotFound(f"Tag with id {tag_id} not found.")
        return ResponseTagDTO(**asdict(tag))

    async def get_filtered_tags(self, name: Optional[str] = None,
                                min_usages: Optional[int] = None,
                                max_usages: Optional[int] = None,
                                with_workout: bool = False) -> Union[
        List[ResponseTagDTO], List[ResponseTagWorkoutDTO]]:
        tags = await self._tag_repository.search_by_constraints(max_usages=max_usages, min_usages=min_usages, name=name,
                                                                with_workout=with_workout)
        if with_workout:
            return [ResponseTagWorkoutDTO(**asdict(tag)) for tag in tags]
        else:
            return [ResponseTagDTO(**asdict(tag)) for tag in tags]

    async def list_tags(self) -> List[ResponseTagDTO]:
        res = await self._tag_repository.list()
        return [ResponseTagDTO(**asdict(r)) for r in res]

    async def update_tag(
            self,
            tag_id: int,
            tag_dto: UpdateTagDTO,
    ) -> ResponseTagDTO:
        async with self._uow:
            db_tag = await self._tag_repository.get(tag_id)
            exiting_tag = await self._tag_repository.get_by_name(tag_dto.name)
            if exiting_tag:
                raise AlreadyExists('Tag with such name already exists')
            if not db_tag:
                raise NotFound(f"Tag with id {tag_id} not found.")
            updated_tag = self._tag_service.update_tag(existing_tag=db_tag, dto=tag_dto)
            await self._tag_repository.update(updated_tag)
            await self._uow.commit()
            return ResponseTagDTO(**asdict(updated_tag))

    async def delete_tag(self, tag_id: int) -> None:
        async with self._uow:
            tag = await self._tag_repository.get(tag_id)
            if not tag:
                raise NotFound(f"Tag with id {tag_id} not found.")
            await self._tag_repository.delete(tag_id)
            await self._uow.commit()
