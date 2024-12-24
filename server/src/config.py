import os
import json
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


class AdminSettings(BaseModel):
    admin_secret_key: str | None = os.environ.get("ADMIN_SECRET_KEY")
    admin_sesion_expire_minutes: int = int(os.environ.get("ADMIN_SESSION_EXPIRE_MINUTES"))  # type: ignore


class RabbitMQSettings(BaseModel):
    user: str = os.environ.setdefault("RABBITMQ_USER", "")
    password: str = os.environ.setdefault("RABBITMQ_PASS", "")
    host: str = os.environ.setdefault("RABBITMQ_HOST", "")
    port: int = int(os.environ.setdefault("RABBITMQ_PORT", ""))
    queue: str = os.environ.setdefault("RABBITMQ_QUEUE", "")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class URLSettings(BaseModel):
    backend_host: str = os.environ.setdefault("BACKEND_HOST", "")
    frontend_host: str = os.environ.setdefault("FRONTEND_HOST", "")


class VerificationSettings(BaseModel):
    secret_key: str = os.environ.setdefault("VERIFICATION_SECRET_KEY", "")
    salt: str = os.environ.setdefault("VERIFICATION_SALT", "")


class CORSSettings(BaseModel):
    allowed_hosts: list[str] = json.loads(os.environ.get("CORS_ALLOWED_HOSTS"))


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    db_settings: DBSettings = DBSettings()
    file_prefixes: FilePrefixes = FilePrefixes()
    storage_settings: StorageSettings = StorageSettings()
    admin_settings: AdminSettings = AdminSettings()
    rabbitmq_settings: RabbitMQSettings = RabbitMQSettings()
    url_settings: URLSettings = URLSettings()
    verification_settings: VerificationSettings = VerificationSettings()
    cors_settings: CORSSettings = CORSSettings()


settings = Settings(
    project_title="Video Hosting API",
    version="0.1.0",
    debug=True,
    description="API for simple video hosting made with Python and FastAPI",
)
