from datetime import datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.core.security import security, verify_token
from app.models.user import User
from app.schemas.token import TokenPayload
from app.schemas.user import UserOut
from app.services.user import UserService

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)

async def get_common_user(
    token: Annotated[Any, Depends(reuseable_oauth)],
    user_service: Annotated[UserService, Depends()],
) -> UserOut:
    user = await _get_token_user(token, settings.SECRET_KEY, user_service)
    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user


async def _get_token_user(
    token: str, key: str, user_service: Annotated[UserService, Depends()]
) -> User:
    try:
        payload = verify_token(token, key)
        token_data = TokenPayload(**payload)
    except (ExpiredSignatureError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_service.get_by_email(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


async def get_refresh_user(
    authorization: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends()],
) -> UserOut:
    return await _get_token_user(
        authorization.credentials, settings.RERFRESH_SECRET_KEY, user_service
    )


async def get_current_admin(
    token: Annotated[Any, Depends(reuseable_oauth)],
    user_service: Annotated[UserService, Depends()],
) -> UserOut:
    user = await _get_token_user(token, settings.SECRET_KEY, user_service)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user
