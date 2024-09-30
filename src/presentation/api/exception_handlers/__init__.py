from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions.base import NotFound, BadRequest
from src.domain.exceptions.base import AlreadyExists
from src.domain.exceptions.base import DataConflict
from src.domain.exceptions.base import InternalServerError

from src.domain.exceptions.jwt import JWTExpiredError
from src.domain.exceptions.jwt import JWTMissingError
from src.domain.exceptions.jwt import JWTSignatureError
from src.domain.exceptions.jwt import JWTDecodeError

from src.domain.exceptions.user import (
    UserDataError,
    InvalidEmailError,
    UserIsNotExistsError,
    IsNotAuthorizedError,
    UserAlreadyExistsError,
    InvalidPasswordError,
    IsNotAdminError
)

from src.presentation.api.exception_handlers.base import (
    value_error_exception_handler,
    unprocessable_entity_exception_handler,
    internal_server_error_exception_handler,
    data_conflict_exception_handler,
    already_exists_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
)

from src.presentation.api.exception_handlers.jwt import (
    jwt_expired_error_exception_handler,
    jwt_missing_error_exception_handler,
    jwt_signature_error_exception_handler,
    jwt_decode_error_exception_handler
)

from src.presentation.api.exception_handlers.user import (
    user_data_exception_handler,
    invalid_email_exception_handler,
    user_is_not_exists_exception_handler,
    is_not_authorized_exception_handler,
    user_already_exists_exception_handler,
    invalid_password_exception_handler,
    is_not_admin_exception_handler
)


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValueError, value_error_exception_handler),
    app.add_exception_handler(UserDataError, user_data_exception_handler)
    app.add_exception_handler(InvalidEmailError, invalid_email_exception_handler)
    app.add_exception_handler(UserIsNotExistsError, user_is_not_exists_exception_handler)
    app.add_exception_handler(IsNotAuthorizedError, is_not_authorized_exception_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_exception_handler)
    app.add_exception_handler(RequestValidationError, unprocessable_entity_exception_handler)
    app.add_exception_handler(InvalidPasswordError, invalid_password_exception_handler)
    app.add_exception_handler(IsNotAdminError, is_not_admin_exception_handler)
    app.add_exception_handler(JWTExpiredError, jwt_expired_error_exception_handler)
    app.add_exception_handler(JWTMissingError, jwt_missing_error_exception_handler)
    app.add_exception_handler(JWTSignatureError, jwt_signature_error_exception_handler)
    app.add_exception_handler(JWTDecodeError, jwt_decode_error_exception_handler)
    app.add_exception_handler(NotFound, not_found_exception_handler)
    app.add_exception_handler(AlreadyExists, already_exists_exception_handler)
    app.add_exception_handler(DataConflict, data_conflict_exception_handler)
    app.add_exception_handler(InternalServerError, internal_server_error_exception_handler)
    app.add_exception_handler(BadRequest, bad_request_exception_handler)
