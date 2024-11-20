import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ServicesSettings(BaseModel):
    s3_storage_service_url: str | None = os.environ.get("S3_STORAGE_SERVICE_URL")
    videos_service_url: str | None = os.environ.get("VIDEOS_SERVICE_URL")
    playlists_service_url: str | None = os.environ.get("PLAYLISTS_SERVICE_URL")


class DBSettings(BaseModel):
    db_host: str | None = os.environ.get("DB_HOST")
    db_port: str | None = os.environ.get("DB_PORT")
    db_name: str | None = os.environ.get("DB_NAME")
    db_user: str | None = os.environ.get("DB_USER")
    db_password: str | None = os.environ.get("DB_PASSWORD")

    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    echo: bool = False


class FilePrefixes(BaseModel):
    profile_photo: str = "PP@"


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    db_settings: DBSettings = DBSettings()
    services: ServicesSettings = ServicesSettings()

    file_prefixes: FilePrefixes = FilePrefixes()


settings = Settings(
    project_title="Users Service API",
    version="0.1.0",
    debug=True,
    description="API for users service",
)
