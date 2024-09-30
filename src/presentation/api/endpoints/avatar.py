from typing import List

from fastapi import APIRouter, Depends, status, UploadFile, File
from starlette.responses import JSONResponse, Response

from src.domain.entities.upload import CreateUpload
from src.presentation.api.dependencies.permissions.user import IsAdminUser, IsAuthenticatedUser
from src.presentation.api.schemas.avatar import Avatar
from src.presentation.interactor_factory import InteractorFactory
from src.application.avatar.dto import CreateAvatarDTO, UpdateAvatarDTO

router = APIRouter(prefix='/avatars', tags=['avatars'])


@router.post('/create', status_code=status.HTTP_201_CREATED, dependencies=[Depends(IsAuthenticatedUser())])
async def create_avatar(upload: UploadFile = File(...), ioc: InteractorFactory = Depends()):
    file_content = await upload.read()

    async with ioc.pick_avatar_interactor(lambda i: i.create_avatar) as interactor:
        response = await interactor(CreateAvatarDTO(
            upload=CreateUpload(
                file=file_content,
                filename=upload.filename,
                filedir='avatars'
            )
        ))

    return {
        'message': 'Avatar successfully created',
        'avatar_id': response.id
    }


@router.get('/list',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=List[Avatar],
            responses={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 1,
                                    "image_url": "http://example.com/avatar1.jpg"
                                },
                                {
                                    "id": 2,
                                    "image_url": "http://example.com/avatar2.jpg"
                                }
                            ]
                        }
                    },
                    "description": "List of all avatars"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No avatars found"
                            }
                        }
                    },
                    "description": "No avatars found"
                }
            },
            summary='List all avatars')
async def get_all_avatars(ioc: InteractorFactory = Depends()):
    async with ioc.pick_avatar_interactor(lambda i: i.get_all_avatars) as interactor:
        response = await interactor()
    return response


@router.get('/{avatar_id}',
            response_model=Avatar,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Avatar retrieved successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Avatar not found"
                            }
                        }
                    },
                    "description": "Avatar not found"
                }
            },
            summary='Get an avatar, only admins or managers')
async def get_avatar(avatar_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_avatar_interactor(lambda i: i.get_avatar_by_id) as interactor:
        response = await interactor(avatar_id)
    return response


@router.put('/{avatar_id}/update',
            status_code=status.HTTP_200_OK,
            response_model=Avatar,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Avatar updated successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Avatar not found"
                            }
                        }
                    },
                    "description": "Avatar not found"
                }
            },
            summary='Update an avatar, only admins or managers')
async def update_avatar(avatar_id: int, upload: UploadFile = File(...), ioc: InteractorFactory = Depends()):
    file_content = await upload.read()
    async with ioc.pick_avatar_interactor(lambda i: i.update_avatar) as interactor:
        response = await interactor(
            avatar_id,
            UpdateAvatarDTO(
                upload=CreateUpload(
                    file=file_content,
                    filename=upload.filename,
                    filedir='avatars'
                )
            )
        )
    return response


@router.delete('/{avatar_id}/delete',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(IsAdminUser())],
               responses={
                   status.HTTP_204_NO_CONTENT: {
                       "description": "Avatar deleted successfully"
                   },
                   status.HTTP_404_NOT_FOUND: {
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Avatar not found"
                               }
                           }
                       },
                       "description": "Avatar not found"
                   }
               },
               summary='Delete an avatar, only admins or managers')
async def delete_avatar(avatar_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_avatar_interactor(lambda i: i.delete_avatar) as interactor:
        await interactor(avatar_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
