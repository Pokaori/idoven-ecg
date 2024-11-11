import asyncio
import uuid
from typing import AsyncGenerator, Generator
from unittest.mock import patch

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
)
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User

engine = create_async_engine(str(settings.TEST_SQLALCHEMY_DATABASE_URI), echo=True)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configure pytest-asyncio
pytest_plugins = ("pytest_asyncio",)


@pytest_asyncio.fixture
def anyio_backend() -> str:
    """Configure async test backend"""
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
def mock_settings():
    """Mock settings for tests"""
    test_settings = {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_PORT": "5672",
        "RABBITMQ_USER": "guest",
        "RABBITMQ_PASSWORD": "guest",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "CELERY_BROKER_URL": "memory://",
        "CELERY_RESULT_BACKEND": "memory://",
    }

    with patch.dict("os.environ", test_settings, clear=False):
        yield


async def override_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    """Create a fresh database session for each test"""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# Create a test client with async support
@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


#Initialize the database
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    app.dependency_overrides[get_db] = override_db
    """Create test database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession):
    """Create test user"""
    # Use a random suffix to ensure email uniqueness
    unique_suffix = str(uuid.uuid4())[:8]
    user = User(
        email=f"test_{unique_suffix}@example.com",
        hashed_password=get_password_hash("StrongPass123!"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def authenticated_user(test_user: User) -> tuple[User, str, str]:
    """Create authenticated user with tokens"""
    # Create access and refresh tokens
    access_token = create_access_token(test_user.email)
    refresh_token = create_refresh_token(test_user.email)

    return test_user, access_token, refresh_token
