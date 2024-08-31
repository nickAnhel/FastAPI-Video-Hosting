import smtplib
import ssl
from typing import Literal
from email.message import EmailMessage
from celery import Celery

from app.config import settings

celery_app = Celery("tasks", broker="redis://redis:6379")


@celery_app.task
def send_console_notification(message: str) -> None:
    print(message)


def get_email_message(data: dict[Literal["To", "Subject", "Content"], str]) -> EmailMessage:
    message = EmailMessage()
    message["To"] = data.get("To")
    message["From"] = settings.smtp.username
    message["Subject"] = data.get("Subject")
    message.set_content(data.get("Content"))
    return message


@celery_app.task
def send_email_notification(data: dict[Literal["To", "Subject", "Content"], str]) -> None:
    message = get_email_message(data)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        host=settings.smtp.host,
        port=settings.smtp.port,
        context=context,
    ) as server:
        server.login(settings.smtp.username, settings.smtp.password)
        server.send_message(message)
