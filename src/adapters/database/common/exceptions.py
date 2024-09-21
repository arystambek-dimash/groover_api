class DatabaseError(Exception):
    pass


class CreateError(DatabaseError):
    pass


class UpdateError(DatabaseError):
    pass


class DeleteError(DatabaseError):
    pass
