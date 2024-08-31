from app.notifications.service import (
    INotificationService,
    ConsoleNotificationsService,
    EmailNotificationsService,
    TelegramNotificationsService,
)


def get_console_notification_service() -> INotificationService:
    return ConsoleNotificationsService()


def get_email_notification_service() -> INotificationService:
    return EmailNotificationsService()


def get_telegram_notification_service() -> INotificationService:
    return TelegramNotificationsService()
