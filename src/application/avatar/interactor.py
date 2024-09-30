from dataclasses import asdict
from typing import List

from src.application.avatar.dto import ResponseAvatarDTO, CreateAvatarDTO, UpdateAvatarDTO
from src.application.interfaces.repository import AvatarRepository
from src.application.interfaces.uow import UoW
from src.domain.entities.avatar import DBAvatar, Avatar
from src.domain.exceptions.base import NotFound, InternalServerError
from src.domain.services.avatar import AvatarService
from src.domain.services.upload import UploadService


class AvatarInteractor:
    def __init__(self,
                 avatar_repository: AvatarRepository,
                 uow: UoW,
                 avatar_service: AvatarService,
                 upload_service: UploadService
                 ):
        self._avatar_repository = avatar_repository
        self._uow = uow
        self._avatar_service = avatar_service
        self._upload_service = upload_service

    async def get_all_avatars(self) -> List[ResponseAvatarDTO]:
        result = await self._avatar_repository.list()
        return [ResponseAvatarDTO(**asdict(r)) for r in result]

    async def get_avatar_by_id(self, avatar_id: int) -> ResponseAvatarDTO:
        db_avatar: DBAvatar = await self._avatar_repository.get(avatar_id)
        if db_avatar is None:
            raise NotFound("Avatar with such id not found")
        return ResponseAvatarDTO(**asdict(db_avatar))

    async def create_avatar(self, avatar: CreateAvatarDTO) -> ResponseAvatarDTO:
        async with self._uow:
            file_path = None
            try:
                file_path = await self._upload_service.upload_file(avatar.upload.file,
                                                                   avatar.upload.filename,
                                                                   avatar.upload.filedir)
                avatar_entity = self._avatar_service.create_avatar(image_url=file_path.url)
                inserted_avatar: DBAvatar = await self._avatar_repository.add(avatar_entity)
                await self._uow.commit()
                return ResponseAvatarDTO(id=inserted_avatar.id, image_url=inserted_avatar.image_url)
            except Exception as e:
                if file_path is not None:
                    await self._upload_service.delete_file(file_path.url)
                await self._uow.rollback()
                print(e)
                raise InternalServerError("Failed to create avatar")

    async def update_avatar(self, avatar_id: int, avatar: UpdateAvatarDTO) -> ResponseAvatarDTO:
        async with self._uow:
            file_path = None
            old_file_path = None

            try:
                db_avatar: DBAvatar = await self._avatar_repository.get(avatar_id)
                if db_avatar is None:
                    raise NotFound("Avatar with such id not found")
                if avatar.upload:
                    old_file_path = db_avatar.image_url

                    file_path = await self._upload_service.upload_file(
                        avatar.upload.file,
                        avatar.upload.filename,
                        avatar.upload.filedir
                    )
                updated_entity = self._avatar_service.update_avatar(
                    db_avatar,
                    Avatar(image_url=file_path.url)
                )
                updated_avatar = await self._avatar_repository.update(updated_entity)
                await self._uow.commit()
                if old_file_path:
                    await self._upload_service.delete_file(old_file_path)
                return ResponseAvatarDTO(**asdict(updated_avatar))
            except Exception as e:
                await self._uow.rollback()
                if file_path:
                    await self._upload_service.delete_file(file_path.url)
                raise InternalServerError(f"Something went wrong while updating avatar: {str(e)}")

    async def delete_avatar(self, avatar_id: int) -> None:
        async with self._uow:
            try:
                db_avatar: DBAvatar = await self._avatar_repository.get(avatar_id)
                if db_avatar is None:
                    raise NotFound("Avatar with such id not found")
                if db_avatar.image_url:
                    await self._upload_service.delete_file(db_avatar.image_url)

                await self._avatar_repository.delete(avatar_id)
                await self._uow.commit()
            except Exception as e:
                await self._uow.rollback()
                raise InternalServerError(f"Something went wrong while deleting avatar: {str(e)}")
