import smtplib
import ssl
from typing import Literal
from email.message import EmailMessage

from app.config import settings
from app.notifications.tasks.app import celery_app


def get_email_message(data: dict[Literal["To", "Subject", "Content"], str]) -> EmailMessage:
    message = EmailMessage()
    message["To"] = data.get("To")
    message["From"] = settings.smtp.username
    message["Subject"] = data.get("Subject")
    message.set_content(data.get("Content"))
    return message


def send_email_message(message: EmailMessage) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        host=settings.smtp.host,
        port=settings.smtp.port,
        context=context,
    ) as server:
        server.login(settings.smtp.username, settings.smtp.password)
        server.send_message(message)


@celery_app.task
def send_email_notification(data: dict[Literal["To", "Subject", "Content"], str]) -> None:
    message = get_email_message(data)
    send_email_message(message)
