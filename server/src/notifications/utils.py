import aio_pika

from src.config import settings
from src.schemas import Email, Telegram


async def send_notification(message: Email | Telegram) -> None:
    try:
        connection = await aio_pika.connect_robust(settings.rabbitmq_settings.url)

        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.model_dump_json().encode()),
                routing_key=settings.rabbitmq_settings.queue,
            )

    except Exception as exc:
        print(exc)
