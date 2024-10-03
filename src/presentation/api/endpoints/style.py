from typing import List, Optional

from fastapi import APIRouter, Depends, status, UploadFile, File
from starlette.responses import JSONResponse, Response

from src.domain.entities.upload import CreateUpload
from src.presentation.api.dependencies.permissions.user import IsAdminUser
from src.presentation.api.dependencies.permissions.user import IsAuthenticatedUser

from src.presentation.api.schemas.style import StyleCreate
from src.presentation.api.schemas.style import StyleUpdate
from src.presentation.api.schemas.style import Style
from src.presentation.api.schemas.style import StyleWithWorkouts

from src.presentation.interactor_factory import InteractorFactory
from src.application.style.dto import CreateStyleDTO, UpdateStyleDTO

router = APIRouter(prefix='/styles', tags=['styles'])


@router.post('/create',
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(IsAdminUser())],
             responses={
                 status.HTTP_201_CREATED: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "message": "Style successfully created",
                                 "style_id": "123"
                             }
                         }
                     },
                     "description": "Style successfully created"
                 },
                 status.HTTP_409_CONFLICT: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Style already exists"
                             }
                         }
                     },
                     "description": "Style already exists"
                 },
                 status.HTTP_404_NOT_FOUND: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Style not found"
                             }
                         }
                     },
                     "description": "Style not found"
                 }
             },
             summary='Create a style, only admins or managers')
async def create_style(style: StyleCreate = Depends(StyleCreate.as_form()),
                       image_file: UploadFile = File(...),
                       ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.create_style) as interactor:
        response = await interactor(CreateStyleDTO(
            name=style.name,
            image_file=CreateUpload(
                file=image_file.file.read(),
                filename=image_file.filename,
                filedir="styles"
            )
        ))

    return JSONResponse(content={
        'message': 'Style successfully created',
        'style_id': response.id
    }, status_code=status.HTTP_201_CREATED)


@router.get('/list',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=List[Style],
            responses={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example":
                                [
                                    {
                                        "id": 1,
                                        "name": "Style 1",
                                        "image_url": "http://example.com/style1.jpg"
                                    },
                                    {
                                        "id": 2,
                                        "name": "Style 2",
                                        "image_url": "http://example.com/style2.jpg"
                                    }
                                ]

                        }
                    },
                    "description": "List of all styles"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No styles found"
                            }
                        }
                    },
                    "description": "No styles found"
                }
            },
            summary='List all styles')
async def get_all_styles(ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.list_styles) as interactor:
        response = await interactor()
    return response


@router.get('/{style_id}',
            response_model=Style,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Style retrieved successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Style not found"
                            }
                        }
                    },
                    "description": "Style not found"
                }
            },
            summary='Get a style, only admins or managers')
async def get_style(style_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.get_style) as interactor:
        response = await interactor(style_id)
    return response


@router.get('/{style_id}/detail',
            status_code=status.HTTP_200_OK,
            response_model=StyleWithWorkouts,
            dependencies=[Depends(IsAuthenticatedUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Style detail retrieved successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Style not found"
                            }
                        }
                    },
                    "description": "Style not found"
                }
            },
            summary='Get a style with workout details, for authenticated users')
async def get_style_detail(style_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.get_style) as interactor:
        response = await interactor(style_id, True)
    print(response)
    return response


@router.put('/{style_id}/update',
            status_code=status.HTTP_200_OK,
            response_model=Style,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Style updated successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Style not found"
                            }
                        }
                    },
                    "description": "Style not found"
                }
            },
            summary='Update a style, only admins or managers')
async def update_style(style_id: int,
                       style: StyleUpdate = Depends(StyleUpdate.as_form()),
                       image_file: Optional[UploadFile] | str = File(None),
                       ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.update_style) as interactor:
        response = await interactor(
            style_id,
            UpdateStyleDTO(
                name=style.name,
                image_file=CreateUpload(
                    file=image_file.file.read(),
                    filename=image_file.filename,
                    filedir="styles"
                ) if image_file else None,
            )
        )
    return response


@router.delete('/{style_id}/delete',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(IsAdminUser())],
               summary='Delete a style, only admins or managers')
async def delete_style(style_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_style_interactor(lambda i: i.delete_style) as interactor:
        response = await interactor(style_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
