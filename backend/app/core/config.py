import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "EduMind"
    API_V1_PREFIX: str = "/v1"
    DEBUG: bool = False

    DATABASE_URL: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "edumind"
    POSTGRES_PASSWORD: str = "edumind_secret"
    POSTGRES_DB: str = "edumind"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_API_KEY: str = ""
    WHISPER_MODEL: str = "small"

    ENABLE_VQA: bool = False
    ENABLE_TABLE_QA: bool = False
    ENABLE_ORAL: bool = False

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def effective_database_url(self) -> str:
        """Return DATABASE_URL from env, or build from components, or fall back to SQLite."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Try Postgres
        pg_url = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return pg_url

    @property
    def effective_sync_database_url(self) -> str:
        """Sync version for Alembic and Celery."""
        url = self.effective_database_url
        # Convert async driver to sync
        url = url.replace("postgresql+asyncpg://", "postgresql://")
        url = url.replace("aiosqlite://", "sqlite://")
        return url

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.effective_database_url

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB + 1}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
