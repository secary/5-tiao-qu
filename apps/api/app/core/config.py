from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = (
        "postgresql+psycopg://five_tiao_qu:five_tiao_qu_dev"
        "@localhost:5432/five_tiao_qu"
    )
    storage_root: Path = Path("../../storage")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    embedding_provider: str = "placeholder"
    embedding_model: str = ""
    embedding_dimensions: int = 1536
    llm_provider: str = "placeholder"
    llm_model: str = ""
    ocr_provider: str = "placeholder"

    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
