from fastapi import Request, responses
from src.domain.exceptions.jwt import (JWTError,
                                       JWTExpiredError,
                                       JWTMissingError,
                                       JWTSignatureError,
                                       JWTDecodeError)


def jwt_error_exception_handler(request: Request, exc: JWTError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )


def jwt_expired_error_exception_handler(request: Request, exc: JWTExpiredError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401,
        content={"detail": "Token has expired"}
    )


def jwt_missing_error_exception_handler(request: Request, exc: JWTMissingError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401,
        content={"detail": "Authentication token is missing"}
    )


def jwt_signature_error_exception_handler(request: Request, exc: JWTSignatureError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401,
        content={"detail": "Invalid token signature"}
    )


def jwt_decode_error_exception_handler(request: Request, exc: JWTDecodeError) -> responses.JSONResponse:
    return responses.JSONResponse(
        status_code=401,
        content={"detail": "Failed to decode token"}
    )
