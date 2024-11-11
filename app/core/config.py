from typing import Any

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ECG Analysis API"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1.0"

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """Convert comma-separated CORS origins string into a list of origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v

    # JWT
    SECRET_KEY: str
    RERFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "app"
    POSTGRES_PORT: str = "5432"

    # Test Database settings
    TEST_POSTGRES_SERVER: str = "localhost"
    TEST_POSTGRES_PORT: str = "5433"
    TEST_POSTGRES_DB: str = "postgres"
    TEST_POSTGRES_PASSWORD: str = "postgres"
    TEST_POSTGRES_USER: str = "postgres"

    # RabbitMQ settings
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: str = "5672"
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    TEST_SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=int(values.data.get("POSTGRES_PORT", 5432)),
            path=values.data.get("POSTGRES_DB") or "",
        )

    @field_validator("TEST_SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_test_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        """Build PostgreSQL DSN for test database connection."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("TEST_POSTGRES_USER"),
            password=values.data.get("TEST_POSTGRES_PASSWORD"),
            host=values.data.get("TEST_POSTGRES_SERVER"),
            port=int(values.data.get("TEST_POSTGRES_PORT", 5432)),
            path=values.data.get("TEST_POSTGRES_DB") or "",
        )

    # Celery settings
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None


    @field_validator("CELERY_BROKER_URL", mode="before")
    def assemble_broker_url(cls, v: str | None, values: dict[str, Any]) -> str | None:
        if v:
            return v
        user = values.data.get("RABBITMQ_USER", "guest")
        password = values.data.get("RABBITMQ_PASSWORD", "guest")
        host = values.data.get("RABBITMQ_HOST", "rabbitmq")
        port = values.data.get("RABBITMQ_PORT", 5672)
        return f"amqp://{user}:{password}@{host}:{port}//"

    @field_validator("CELERY_RESULT_BACKEND", mode="before")
    def assemble_backend_url(cls, v: str | None, values: dict[str, Any]) -> str | None:
        if v:
            return v
        user = values.data.get("POSTGRES_USER", "postgres")
        password = values.data.get("POSTGRES_PASSWORD", "postgres")
        server = values.data.get("POSTGRES_SERVER", "db")
        port = values.data.get("POSTGRES_PORT", 5432)
        db = values.data.get("POSTGRES_DB", "postgres")
        return f"db+postgresql://{user}:{password}@{server}:{port}/{db}"

    model_config = SettingsConfigDict(env_file=(".env", ".docker.env"), extra="ignore")


settings = Settings()
