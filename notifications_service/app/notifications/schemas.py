from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

from app.notifications.enums import NotificationTypes


TelegramLink = Annotated[
    str,
    Field(
        examples=["https://t.me/username"],
        pattern="^https://t\\.me/[a-zA-Z0-9_]{5,32}$",
    ),
]


class BaseNotification(BaseModel):
    content: str


class ConsoleNotification(BaseNotification):
    username: str
    notification_type: NotificationTypes


class EmailNotification(BaseNotification):
    email: EmailStr
    subject: str = Field(max_length=50)


class TelegramNotification(BaseNotification):
    link: TelegramLink
