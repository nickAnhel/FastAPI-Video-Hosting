from pydantic import BaseModel, ConfigDict


class SettingsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SettingsGet(SettingsBase):
    enable_telegram_notifications: bool
    enable_email_notifications: bool


class SettingsUpdate(SettingsBase):
    enable_telegram_notifications: bool | None = None
    enable_email_notifications: bool | None = None
