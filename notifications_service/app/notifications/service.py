from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from app.notifications.schemas import (
    ConsoleNotification,
    EmailNotification,
    TelegramNotification,
)
from app.notifications.tasks import send_console_notification, send_email_notification
from app.notifications.templates import notification_templates


Notification = TypeVar("Notification")


class INotificationService(Generic[Notification], ABC):
    @abstractmethod
    def send_notification(self, notification: Notification) -> None:
        raise NotImplementedError


class ConsoleNotificationsService(INotificationService):
    def send_notification(self, notification: ConsoleNotification) -> None:
        message = notification_templates.console_notification_template.format(
            username=notification.username,
            notification_type=notification.notification_type,
            content=notification.content,
        )

        send_console_notification.delay(message)


class EmailNotificationsService(INotificationService):
    def send_notification(self, notification: EmailNotification) -> None:
        data = {
            "To": notification.email,
            "Subject": notification.subject,
            "Content": notification.content,
        }

        send_email_notification.delay(data)


class TelegramNotificationsService(INotificationService):
    def send_notification(self, notification: TelegramNotification) -> None:
        pass
