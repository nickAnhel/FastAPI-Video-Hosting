from pydantic import BaseModel, ConfigDict

from src.schemas import BaseSchema


class SettingsGet(BaseSchema):
    enable_telegram_notifications: bool
    enable_email_notifications: bool


class SettingsUpdate(BaseSchema):
    enable_telegram_notifications: bool | None = None
    enable_email_notifications: bool | None = None
