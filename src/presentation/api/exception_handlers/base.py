from fastapi import Request, responses
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions.base import (
    InternalServerError,
    DataConflict,
    AlreadyExists,
    NotFound, BadRequest
)


async def unprocessable_entity_exception_handler(
        _request: Request, _exc: RequestValidationError
) -> responses.JSONResponse:
    print(_exc)
    return responses.JSONResponse(
        status_code=422,
        content={"detail": "The provided data is invalid. Please check your input."},
    )


async def value_error_exception_handler(
        _request: Request, _exc: ValueError
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=409,
        content={"detail": str(_exc)},
    )


def not_found_exception_handler(request: Request, exc: NotFound) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=404,
        content={"detail": str(exc) or "Resource not found"}
    )


def already_exists_exception_handler(request: Request, exc: AlreadyExists) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=409,
        content={"detail": str(exc) or "Resource already exists"}
    )


def data_conflict_exception_handler(request: Request, exc: DataConflict) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=409,
        content={"detail": str(exc) or "Data conflict occurred"}
    )


def internal_server_error_exception_handler(request: Request, exc: InternalServerError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=500,
        content={"detail": str(exc) or "Internal server error occurred"}
    )


def bad_request_exception_handler(request: Request, exc: BadRequest) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
