from fastapi import Request, responses

from src.domain.exceptions.user import (
    UserDataError,
    UserIsNotExistsError,
    IsNotAuthorizedError,
    UserAlreadyExistsError,
    InvalidPasswordError,
    InvalidEmailError, IsNotAdminError,
)


async def user_data_exception_handler(
        _request: Request, _exc: UserDataError,
) -> responses.JSONResponse:
    return responses.JSONResponse(status_code=422, content={"detail": str(_exc)})


async def invalid_email_exception_handler(
        _request: Request, _exc: InvalidEmailError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=422, content={"detail": "Неверный формат email"},
    )


async def user_is_not_exists_exception_handler(
        _request: Request, _exc: UserIsNotExistsError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401, content={"detail": "Пользователь не существует"},
    )


async def is_not_authorized_exception_handler(
        _request: Request, _exc: IsNotAuthorizedError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401, content={"detail": "Вы не авторизованы"},
    )


async def user_already_exists_exception_handler(
        _request: Request, _exc: UserAlreadyExistsError,
) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=409, content={"detail": "Пользователь уже существует"},
    )


async def invalid_password_exception_handler(
        _request: Request, _exc: InvalidPasswordError
):
    return responses.JSONResponse(
        status_code=400,
        content={"detail": str(_exc)},
    )


async def is_not_admin_exception_handler(
        _request: Request, _exc: IsNotAdminError
):
    return responses.JSONResponse(
        status_code=403,
        content={"detail": str(_exc)},
    )
