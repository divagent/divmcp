from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DIVCORE_BASE_URL: str = "http://127.0.0.1:8000"
    DIVCORE_AUTH_USERNAME: str = "mcp"
    DIVCORE_ADMIN_PASSWORD: str = "admin123"
    DIVCORE_TIMEOUT_SECONDS: float = 30.0


@lru_cache()
def get_settings() -> Settings:
    return Settings()
