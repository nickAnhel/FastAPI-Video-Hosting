import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class SMTPSettings(BaseModel):
    host: str = os.environ.setdefault("SMTP_HOST", "")
    port: int = int(os.environ.setdefault("SMTP_PORT", ""))
    username: str = os.environ.setdefault("SMTP_USERNAME", "")
    password: str = os.environ.setdefault("SMTP_PASSWORD", "")


class TelegramSettings(BaseModel):
    token: str = os.environ.setdefault("TELEGRAM_TOKEN", "")


class Settings(BaseSettings):
    project_title: str
    version: str
    debug: bool
    description: str

    smtp: SMTPSettings = SMTPSettings()
    telegram: TelegramSettings = TelegramSettings()


settings = Settings(
    project_title="Notifications Service API",
    version="0.1.0",
    debug=True,
    description="API for notifications service",
)
