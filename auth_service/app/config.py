from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class ServiceSettings(BaseSettings):
    users_service_url: str | None = None

    model_config = SettingsConfigDict(env_file=".docker-env")


class AuthSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    auth_settings: AuthSettings = AuthSettings()

    services: ServiceSettings = ServiceSettings()

settings = Settings(
    project_title="Auth Service API",
    version="0.1.0",
    debug=True,
    description="API for auth service",
)
