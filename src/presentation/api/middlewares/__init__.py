from fastapi import FastAPI

from src.presentation.api.middlewares.upload_file_middleware import MaxFileSizeMiddleware


def include_middlewares(app: FastAPI) -> None:
    """Include middlewares main app"""
    app.add_middleware(MaxFileSizeMiddleware)
