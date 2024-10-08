from typing import List, Union

from fastapi import APIRouter, Depends, status, Query
from starlette.responses import JSONResponse, Response

from src.application.tag.interactor import TagInteractor
from src.domain.entities.pagination import PaginatedResponseDTO
from src.presentation.api.dependencies.permissions.user import IsAdminUser, IsAuthenticatedUser
from src.presentation.interactor_factory import InteractorFactory
from src.application.tag.dto import CreateTagDTO, UpdateTagDTO
from src.presentation.api.schemas.tag import TagCreate, TagUpdate, Tag, TagWorkouts, PaginatedTag

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
            dependencies=[Depends(IsAdminUser())],
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
            summary='List all tags, for admins and managers')
async def get_all_tags(ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.list_tags) as interactor:
        response = await interactor()
    return response


@router.get('/search/by-name',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=List[Tag],
            summary='Search tags by name, with option to include workouts')
async def get_tags_by_name(name: str, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_filtered_tags) as interactor:
        response = await interactor(name=name)
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
        response = await interactor(tag_id, False)
    return response


@router.get('/list/paginated',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=PaginatedTag,
            summary='List paginated tags')
async def get_tags_paginated(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        ioc: InteractorFactory = Depends()
):
    async with ioc.pick_tag_interactor(lambda i: i.list_tags) as interactor:
        response = await interactor(page, limit)
    return response


@router.get('/list/popular',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=PaginatedTag,
            summary='List popular tags with pagination')
async def get_popular_tags_paginated(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1),
        ioc: InteractorFactory = Depends()
):
    async with ioc.pick_tag_interactor(lambda i: i.list_popular_tags) as interactor:
        response = await interactor(page, limit)
    return response


@router.get('/{tag_id}/detial',
            response_model=TagWorkouts,
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
            summary='Get a tag with detail')
async def get_tag(tag_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_tag_interactor(lambda i: i.get_tag) as interactor:
        response = await interactor(tag_id, True)
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
