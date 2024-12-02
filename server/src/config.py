import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DBSettings(BaseModel):
    db_host: str | None = os.environ.get("DB_HOST")
    db_port: str | None = os.environ.get("DB_PORT")
    db_name: str | None = os.environ.get("DB_NAME")
    db_user: str | None = os.environ.get("DB_USER")
    db_password: str | None = os.environ.get("DB_PASSWORD")

    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    echo: bool = False


class StorageSettings(BaseModel):
    access_key: str | None = os.getenv("ACCESS_KEY")
    secret_key: str | None = os.getenv("SECRET_KEY")
    bucket_name: str | None = os.getenv("BUCKET_NAME")
    bucket_url: str | None = os.getenv("BUCKET_URL")
    storage_url: str | None = os.getenv("STORAGE_URL")


class FilePrefixes(BaseModel):
    profile_photo_small: str = "PPs@"
    profile_photo_medium: str = "PPm@"
    profile_photo_large: str = "PPl@"

    video: str = "VV@"
    preview: str = "VP@"


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    db_settings: DBSettings = DBSettings()
    file_prefixes: FilePrefixes = FilePrefixes()
    storage_settings: StorageSettings = StorageSettings()


settings = Settings(
    project_title="Video Hosting API",
    version="0.1.0",
    debug=True,
    description="API for simple video hosting made with Python and FastAPI",
)