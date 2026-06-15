from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_db: str = "voice_agent"
    postgres_user: str = "voice_agent"
    postgres_password: str = "voice_agent_dev"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    backend_cors_origins: str = "http://localhost:4200"
    secret_key: str = "change-me"
    n8n_webhook_secret: str = "change-me"

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

