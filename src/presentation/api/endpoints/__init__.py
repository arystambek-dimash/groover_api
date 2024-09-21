from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions.user import (UserDataError,
                                        UserIsNotExistsError,
                                        IsNotAuthorizedError,
                                        InvalidEmailError,
                                        UserAlreadyExistsError,
                                        InvalidPasswordError,
                                        IsNotAdminError)
from src.presentation.api.endpoints import user
from src.presentation.api.exception_handlers.user import (
    user_data_exception_handler,
    user_is_not_exists_exception_handler,
    is_not_authorized_exception_handler,
    invalid_email_exception_handler,
    user_already_exists_exception_handler,
    value_error_exception_handler,
    unprocessable_entity_exception_handler,
    invalid_password_exception_handler,
    is_not_admin_exception_handler
)


def include_routers(app: FastAPI) -> None:
    """Include endpoints APIRouters to the main app"""

    app.include_router(user.router)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserDataError, user_data_exception_handler)
    app.add_exception_handler(InvalidEmailError, invalid_email_exception_handler)
    app.add_exception_handler(UserIsNotExistsError, user_is_not_exists_exception_handler)
    app.add_exception_handler(IsNotAuthorizedError, is_not_authorized_exception_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_exception_handler)
    app.add_exception_handler(ValueError, value_error_exception_handler),
    app.add_exception_handler(RequestValidationError, unprocessable_entity_exception_handler)
    app.add_exception_handler(InvalidPasswordError, invalid_password_exception_handler)
    app.add_exception_handler(IsNotAdminError, is_not_admin_exception_handler)
