from fastapi import FastAPI

from src.presentation.api.endpoints import user
from src.presentation.api.endpoints import style
from src.presentation.api.endpoints import tag
from src.presentation.api.endpoints import workout
from src.presentation.api.endpoints import avatar


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the main app"""
    app.include_router(user.router, prefix='/api')
    app.include_router(style.router, prefix='/api')
    app.include_router(tag.router, prefix='/api')
    app.include_router(workout.router, prefix='/api')
    app.include_router(avatar.router, prefix='/api')
