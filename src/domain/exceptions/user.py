class UserDataError(Exception):
    pass


class InvalidEmailError(Exception):
    pass


class IsNotAdminError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class UserIsNotExistsError(Exception):
    pass


class IsNotAuthorizedError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass
