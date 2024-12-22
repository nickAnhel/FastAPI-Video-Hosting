import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class SMTPSettings(BaseModel):
    host: str = os.environ.setdefault("SMTP_HOST", "")
    port: int = int(os.environ.setdefault("SMTP_PORT", ""))
    username: str = os.environ.setdefault("SMTP_USERNAME", "")
    password: str = os.environ.setdefault("SMTP_PASSWORD", "")


class RabbitMQSettings(BaseModel):
    user: str = os.environ.setdefault("RABBITMQ_USER", "")
    password: str = os.environ.setdefault("RABBITMQ_PASS", "")
    host: str = os.environ.setdefault("RABBITMQ_HOST", "")
    port: int = int(os.environ.setdefault("RABBITMQ_PORT", ""))
    queue: str = os.environ.setdefault("RABBITMQ_QUEUE", "")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class TelegramSettings(BaseModel):
    token: str = os.environ.setdefault("TELEGRAM_TOKEN", "")


class Settings(BaseSettings):
    smtp: SMTPSettings = SMTPSettings()
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    telegram: TelegramSettings = TelegramSettings()


settings = Settings()
