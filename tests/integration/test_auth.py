import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user import UserService


@pytest.mark.asyncio
async def test_register_login_flow(client: AsyncClient, authenticated_admin_user: tuple[User, str, str]):
    # Test data

    _, access_token, _ = authenticated_admin_user
    user_data = {"email": "test@example.com", "password": "Test123!@#"}

    # Test registration
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/api/v1/auth/register", json=user_data, headers=headers)
    assert response.status_code == 200
    user_response = response.json()
    assert user_response["email"] == user_data["email"]
    assert "id" in user_response

    # Test login
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, authenticated_admin_user: tuple[User, str, str]):
    # Test data
    _, access_token, _ = authenticated_admin_user
    user_data = {"email": "duplicate@example.com", "password": "Test123!@#"}

    headers = {"Authorization": f"Bearer {access_token}"}
    # Register first user
    response = await client.post("/api/v1/auth/register", json=user_data, headers=headers)
    assert response.status_code == 200

    # Try to register with same email
    response = await client.post("/api/v1/auth/register", json=user_data, headers=headers)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {"username": "nonexistent@example.com", "password": "WrongPass123!@#"}
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@pytest.mark.asyncio
async def test_refresh_token(
    client: AsyncClient, authenticated_user: tuple[User, str, str]
):
    # Get refresh token from authenticated user
    user, _, refresh_token = authenticated_user

    # Use refresh token to get new access token
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = await client.get("/api/v1/auth/refresh", headers=headers)

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data


@pytest.mark.asyncio
async def test_password_invalid(client: AsyncClient, authenticated_admin_user: tuple[User, str, str]):
    # Test with weak password
    _, access_token, _ = authenticated_admin_user
    user_data = {
        "email": "test@example.com",
        "password": "weakpass",  # Missing uppercase, number, and special char
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/api/v1/auth/register", json=user_data, headers=headers)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_as_normal_user_fails(client: AsyncClient, authenticated_user: tuple[User, str, str]):
    """Test that normal users cannot register new users"""
    # Get normal user's access token
    _, access_token, _ = authenticated_user
    
    # Try to register a new user
    new_user_data = {"email": "newuser@example.com", "password": "Test123!@#"}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = await client.post("/api/v1/auth/register", json=new_user_data, headers=headers)
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]
