from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")
security = HTTPBearer(description="To refresh token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def __create_token(
    subject: str, minutes: int, key: str, expires_delta: int | None = None
):
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key, settings.ALGORITHM)
    return encoded_jwt


def create_access_token(subject: str, expires_delta: int = None) -> str:
    return __create_token(
        subject,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        settings.SECRET_KEY,
        expires_delta,
    )


def create_refresh_token(subject: str, expires_delta: int = None) -> str:
    return __create_token(
        subject,
        settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        settings.RERFRESH_SECRET_KEY,
        expires_delta,
    )


def verify_token(token: str, key: str) -> dict[str, Any]:
    return jwt.decode(token, key, algorithms=[settings.ALGORITHM])
