from typing import List, Union

from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse, Response
from src.presentation.api.dependencies.permissions.user import IsAdminUser, IsAuthenticatedUser
from src.presentation.interactor_factory import InteractorFactory
from src.application.tag.dto import CreateTagDTO, UpdateTagDTO
from src.presentation.api.schemas.tag import TagCreate, TagUpdate, Tag, TagWorkouts

router = APIRouter(prefix='/tags', tags=['tags'])


@router.post('/create',
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(IsAdminUser())],
             responses={
                 status.HTTP_201_CREATED: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "message": "Tag successfully created",
                                 "tag_id": "123"
                             }
                         }
                     },
                     "description": "Tag successfully created"
                 },
                 status.HTTP_409_CONFLICT: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Tag already exists"
                             }
                         }
                     },
                     "description": "Tag already exists"
                 }
             },
             summary='Create a tag, only admins or managers')
async def create_tag(tag: TagCreate, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.create_tag) as interactor:
        response = await interactor(CreateTagDTO(
            name=tag.name,
        ))

    return JSONResponse(content={
        'message': 'Tag successfully created',
        'tag_id': response.id
    }, status_code=status.HTTP_201_CREATED)


@router.get('/list',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=List[Tag],
            responses={
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tags found"
                            }
                        }
                    },
                    "description": "No tags found"
                }
            },
            summary='List all tags')
async def get_all_tags(ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.list_tags) as interactor:
        response = await interactor()
    return response


@router.get('/search/by-name',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=Union[List[TagWorkouts], List[Tag]],
            summary='Search tags by name, with option to include workouts')
async def get_tags_by_name(with_workout: bool, name: str, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_filtered_tags) as interactor:
        response = await interactor(name=name, with_workout=with_workout)
    return response


@router.get('/search/by-min-usages',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=Union[List[TagWorkouts], List[Tag]],
            summary='Search tags by minimum usages, with option to include workouts')
async def get_tags_by_min_usages(min_usages: int, with_workout: bool = False, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_filtered_tags) as interactor:
        response = await interactor(min_usages=min_usages, with_workout=with_workout)
    return response


@router.get('/search/by-max-usages',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=Union[List[TagWorkouts], List[Tag]],
            summary='Search tags by maximum usages, with option to include workouts')
async def get_tags_by_max_usages(max_usages: int, with_workout: bool = False, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_filtered_tags) as interactor:
        response = await interactor(max_usages=max_usages, with_workout=with_workout)
    return response


@router.get('/{tag_id}',
            response_model=Tag,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Tag retrieved successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Tag not found"
                            }
                        }
                    },
                    "description": "Tag not found"
                }
            },
            summary='Get a tag, only admins or managers')
async def get_tag(tag_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_tag) as interactor:
        response = await interactor(tag_id)
    return response


@router.put('/{tag_id}/update',
            response_model=Tag,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Tag updated successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Tag not found"
                            }
                        }
                    },
                    "description": "Tag not found"
                }
            },
            summary='Update a tag, only admins or managers')
async def update_tag(tag_id: int, tag: TagUpdate, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.update_tag) as interactor:
        response = await interactor(tag_id, UpdateTagDTO(name=tag.name))
    return response


@router.delete('/{tag_id}/delete',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(IsAdminUser())],
               responses={
                   status.HTTP_204_NO_CONTENT: {
                       "description": "Tag deleted successfully",
                       "content": {
                           "application/json": {
                               "example": {
                                   "message": "Tag deleted successfully"
                               }
                           }
                       }
                   },
                   status.HTTP_404_NOT_FOUND: {
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Tag not found"
                               }
                           }
                       },
                       "description": "Tag not found"
                   }
               },
               summary='Delete a tag, only admins or managers')
async def delete_tag(tag_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.delete_tag) as interactor:
        await interactor(tag_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
