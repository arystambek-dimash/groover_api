from typing import List, Optional
from starlette.responses import JSONResponse, Response
from fastapi import APIRouter, Depends, status, UploadFile, File, Form

from src.domain.entities.upload import CreateUpload
from src.presentation.api.dependencies.permissions.user import IsAdminUser, IsAuthenticatedUser
from src.presentation.interactor_factory import InteractorFactory

from src.application.workout.dto import (
    WorkoutCreateDTO,
    WorkoutUpdateDTO
)
from src.presentation.api.schemas.workout import (
    WorkoutCreate,
    WorkoutUpdate,
    Workout, WorkoutViewResponse, WorkoutWithStyle
)

router = APIRouter(prefix='/workouts', tags=['workouts'])


@router.post('/create',
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(IsAdminUser())],
             responses={
                 status.HTTP_201_CREATED: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "message": "Workout successfully created",
                                 "workout_id": 123
                             }
                         }
                     },
                     "description": "Workout successfully created"
                 },
                 status.HTTP_409_CONFLICT: {
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Workout already exists"
                             }
                         }
                     },
                     "description": "Workout already exists"
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
             summary='Create a workout, only admins or managers')
async def create_workout(workout: WorkoutCreate = Depends(WorkoutCreate.as_form()),
                         thumbnail_image: UploadFile = File(...),
                         ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.create_workout) as interactor:
        response = await interactor(WorkoutCreateDTO(
            name=workout.name,
            calories=workout.calories,
            duration=workout.duration,
            level=workout.level,
            description=workout.description,
            dance_video=workout.dance_video,
            thumbnail_image=CreateUpload(
                file=thumbnail_image.file.read(),
                filename=thumbnail_image.filename,
                filedir='workouts/images'
            ),
            author_name=workout.author_name,
            style_id=workout.style_id,
            tags=workout.tags[0].split(',')
        ))
    return JSONResponse(content={
        'message': 'Workout successfully created',
        'workout_id': response.id
    }, status_code=status.HTTP_201_CREATED)


@router.get('/list',
            dependencies=[Depends(IsAuthenticatedUser())],
            response_model=List[WorkoutWithStyle],
            responses={
                status.HTTP_200_OK: {
                    "description": "List of all workouts"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No workouts found"
                            }
                        }
                    },
                    "description": "No workouts found"
                }
            },
            summary='List all workouts')
async def list_workouts(ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.list_workouts) as interactor:
        workouts = await interactor()
    return workouts


@router.get('/{workout_id}',
            response_model=Workout,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAuthenticatedUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Workout retrieved successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Workout not found"
                            }
                        }
                    },
                    "description": "Workout not found"
                }
            },
            summary='Get a workout, accessible to authenticated users')
async def get_workout(workout_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.get_workout) as interactor:
        workout = await interactor(workout_id)
    return workout


@router.put('/{workout_id}/update',
            response_model=Workout,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(IsAdminUser())],
            responses={
                status.HTTP_200_OK: {
                    "description": "Workout updated successfully"
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Workout not found"
                            }
                        }
                    },
                    "description": "Workout not found"
                }
            },
            summary='Update a workout, only admins or managers')
async def update_workout(
        workout_id: int,
        workout: WorkoutUpdate = Depends(WorkoutUpdate.as_form()),
        thumbnail_image: Optional[UploadFile] | str = File(None),
        ioc: InteractorFactory = Depends()
):
    if thumbnail_image and thumbnail_image.filename:
        file_content = await thumbnail_image.read()
        create_upload = CreateUpload(
            file=file_content,
            filename=thumbnail_image.filename,
            filedir='workouts/images'
        )
    else:
        create_upload = None
    async with ioc.pick_workout_interactor(lambda i: i.update_workout) as interactor:
        updated_workout = await interactor(workout_id, WorkoutUpdateDTO(
            name=workout.name,
            calories=int(workout.calories) if workout.calories is not None else None,
            duration=int(workout.duration) if workout.duration is not None else None,
            level=workout.level,
            description=workout.description,
            dance_video=workout.dance_video,
            thumbnail_image=create_upload,
            author_name=workout.author_name
        ))
    return updated_workout


@router.put('/workout/update-views',
            response_model=WorkoutViewResponse,
            dependencies=[Depends(IsAuthenticatedUser())])
async def update_workout_views(workout_id: int = Form(), ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.update_workout_views) as interactor:
        workout = await interactor(
            workout_id
        )
    return workout


@router.delete('/{workout_id}/delete',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(IsAdminUser())],
               responses={
                   status.HTTP_204_NO_CONTENT: {
                       "description": "Workout deleted successfully"
                   },
                   status.HTTP_404_NOT_FOUND: {
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Workout not found"
                               }
                           }
                       },
                       "description": "Workout not found"
                   }
               },
               summary='Delete a workout, only admins or managers')
async def delete_workout(workout_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.delete_workout) as interactor:
        await interactor(workout_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/{workout_id}/add-tag', dependencies=[Depends(IsAdminUser())])
async def add_tag_for_workout(workout_id: int, tags: List[str], ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.add_tag_for_workout) as interactor:
        res = await interactor(workout_id, tags)
    message = {
        "message": "Tags added successfully" if res else "Something went wrong"
    }
    return message


@router.delete('/{workout_id}/delete/{tag_id}/tag', dependencies=[Depends(IsAdminUser())])
async def delete_tag_from_workout(workout_id: int, tag_id: int, ioc: InteractorFactory = Depends()):
    async with ioc.pick_workout_interactor(lambda i: i.delete_tag_from_workout) as interactor:
        res = await interactor(workout_id, tag_id)
    message = {
        "message": "Tag deleted successfully" if res else "Something went wrong",
    }
    return message
