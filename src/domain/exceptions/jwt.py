class JWTError(Exception):
    """Base class for JWT-related exceptions."""
    pass


class JWTDecodeError(JWTError):
    """Raised when the JWT cannot be decoded."""
    pass


class JWTExpiredError(JWTError):
    """Raised when the JWT has expired."""
    pass


class JWTSignatureError(JWTError):
    """Raised when the JWT signature is invalid."""
    pass


class JWTMissingError(JWTError):
    """Raised when the JWT is missing from the request."""
    pass
