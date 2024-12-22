import ssl
import smtplib
import asyncio
import httpx
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery


from config import settings
from schemas import Email, Telegram


app = Celery("tasks", broker=settings.rabbitmq.url, backend="rpc://")


def get_email_message(data: Email) -> MIMEMultipart:
    message = MIMEMultipart("alternative")

    message["To"] = data.email
    message["From"] = settings.smtp.username
    message["Subject"] = data.subject

    html_text = MIMEText(data.content, "html")
    message.attach(html_text)
    return message


def send_email_message(message: MIMEMultipart) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        host=settings.smtp.host,
        port=settings.smtp.port,
        context=context,
    ) as server:
        server.login(settings.smtp.username, settings.smtp.password)
        server.send_message(message)


@app.task
def send_email_notification(data: dict) -> None:
    email_data = Email.model_validate(data)
    message = get_email_message(email_data)
    send_email_message(message)


async def send_telegram_message(data: Telegram) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{settings.telegram.token}/sendPhoto",
            data={
                "chat_id": data.chat_id,
                "photo": data.preview_url,
                "caption": data.content,
                "parse_mode": "HTML",
            },
        )


@app.task
def send_telegram_notification(data: dict) -> None:
    telegram_data = Telegram.model_validate(data)
    asyncio.run(send_telegram_message(telegram_data))
