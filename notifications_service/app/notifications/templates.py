from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationTemplates:
    console_notification_template: str = "\nConsole Notification\nTo: {username}\nType: {notification_type}\nContent: {content}\n"


notification_templates = NotificationTemplates()
