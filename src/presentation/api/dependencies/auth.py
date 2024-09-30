from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.config import settings
from src.domain.entities.user import DBUser
from src.application.user.jwt import JWTService
from src.adapters.database.provider import get_user_repository
from src.presentation.api.dependencies.db import get_db_session

from src.domain.exceptions.jwt import (
    JWTError,
    JWTExpiredError,
    JWTMissingError,
    JWTSignatureError,
    JWTDecodeError
)

security = HTTPBearer()


async def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials:
        return credentials.credentials
    else:
        raise JWTMissingError("Missing authentication token")


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
            raise JWTError("Invalid token payload")
        user = await user_repository.get(user_id)
        if not user:
            raise JWTError("User not found")
        return user
    except JWTExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature",
        )
    except JWTDecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode token",
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
