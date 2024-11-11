from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_refresh_user
from app.core.security import create_access_token, create_refresh_token
from app.schemas.token import Token, TokenAccess
from app.schemas.user import UserCreate, UserOut
from app.services.user import UserService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends()],
):
    """
    Login for access token.
    """
    user = await user_service.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserOut)
async def register(
    user_create: UserCreate, user_service: Annotated[UserService, Depends()]
):
    """
    Create new user (admin only).
    """
    existing_user = await user_service.get_by_email(user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await user_service.create(user_create)


@router.get("/refresh", response_model=TokenAccess)
async def refresh_token(user: Annotated[UserOut, Depends(get_refresh_user)]):
    """
    Refresh access token using refresh token.
    """
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}
