from typing import TypeVar

from src.domain.entities.workout import Workout, DBWorkout

T = TypeVar('T')


class WorkoutService:
    @staticmethod
    def update_workout(existing_workout: DBWorkout, dto: Workout) -> DBWorkout:
        return DBWorkout(
            id=existing_workout.id,
            name=dto.name if dto.name else existing_workout.name,
            calories=dto.calories if dto.calories else existing_workout.calories,
            duration=dto.duration if dto.duration else existing_workout.duration,
            level=dto.level if dto.level else existing_workout.level,
            description=dto.description if dto.description else existing_workout.description,
            dance_video=dto.dance_video if dto.dance_video else existing_workout.dance_video,
            thumbnail_image=dto.thumbnail_image if dto.thumbnail_image else existing_workout.thumbnail_image,
            author_name=dto.author_name if dto.author_name else existing_workout.author_name,
            views_count=existing_workout.views_count,
            style_id=dto.style_id if dto.style_id else existing_workout.style_id,
            tags=None
        )

    @staticmethod
    def create_workout_entity(dto: T) -> Workout:
        return Workout(
            name=dto.name,
            calories=dto.calories,
            duration=dto.duration,
            level=dto.level,
            description=dto.description,
            dance_video=dto.dance_video,
            thumbnail_image=dto.thumbnail_image,
            author_name=dto.author_name,
            views_count=0,
            style_id=dto.style_id,
            tags=dto.tags
        )
