from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.auth.jwt_service import JWTService
from src.adapters.database.provider import get_user_repository
from src.domain.exceptions.jwt import InvalidCredentialsError
from src.domain.entities.user import DBUser
from src.main.config import settings
from src.presentation.api.dependencies.db import get_db_session

security = HTTPBearer()


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials:
        return credentials.credentials
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_current_user(
        token: str = Depends(get_token),
        session: AsyncSession = Depends(get_db_session),
) -> DBUser:
    jwt_service = JWTService(settings.jwt.jwt_secret_key)
    user_repository = get_user_repository(session)
    try:
        payload = jwt_service.decode(token)
        user_id = payload.sub
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
