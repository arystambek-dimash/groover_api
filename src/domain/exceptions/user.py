from src.domain.exceptions.base import DomainError


class UserDataError(DomainError):
    pass


class InvalidEmailError(DomainError):
    pass


class IsNotAdminError(DomainError):
    pass


class InvalidPasswordError(DomainError):
    pass


class UserIsNotExistsError(DomainError):
    pass


class IsNotAuthorizedError(DomainError):
    pass


class UserAlreadyExistsError(DomainError):
    pass
