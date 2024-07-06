from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    access_key: str | None = None
    secret_key: str | None = None
    bucket_name: str | None = None
    bucket_url: str | None = None
    storage_url: str | None = None

    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"))


settings = Settings(
    project_title="S3 Storage Service API",
    version="0.1.0",
    debug=True,
    description="API for S3 storage service",
)
