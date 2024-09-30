from fastapi import Depends

from src.domain.entities.user import DBUser
from src.presentation.api.dependencies.auth import get_current_user


class IsAdminUser:
    def __call__(self, user: DBUser = Depends(get_current_user)) -> bool:
        if user and user.role in ['ADMIN', 'MANAGER']:
            return True
        return False


class IsAuthenticatedUser:
    def __call__(self, user: DBUser = Depends(get_current_user)) -> bool:
        if user:
            return True
        return False
