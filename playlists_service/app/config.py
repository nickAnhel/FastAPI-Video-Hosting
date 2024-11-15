import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class ServicesSettings(BaseModel):
    auth_users_service_url: str | None = os.environ.get("AUTH_USERS_SERVICE_URL")


class DBSettings(BaseModel):
    db_host: str | None = os.environ.get("DB_HOST")
    db_port: str | None = os.environ.get("DB_PORT")
    db_name: str | None = os.environ.get("DB_NAME")
    db_user: str | None = os.environ.get("DB_USER")
    db_password: str | None = os.environ.get("DB_PASSWORD")

    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    echo: bool = False


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    services: ServicesSettings = ServicesSettings()
    db_settings: DBSettings = DBSettings()

    prohibited_names: list[str] = ["Watch History", "Liked Videos", "Disliked Videos"]


settings = Settings(
    project_title="Playlists Service API",
    version="0.1.0",
    debug=True,
    description="API for playlists service",
)
