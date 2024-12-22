import json
import asyncio
import aio_pika

from config import settings
from tasks import send_email_notification, send_telegram_notification


async def main():
    connection = await aio_pika.connect_robust(settings.rabbitmq.url)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.rabbitmq.queue, durable=True)

        async for message in queue:
            async with message.process():
                message_body = json.loads(message.body)

                match message_body.get("type"):
                    case "email":
                        send_email_notification.delay(message_body)

                    case "telegram":
                        send_telegram_notification.delay(message_body)

                    case _:
                        print(f"Unknown message type: {message_body.get("type")}")


if __name__ == "__main__":
    asyncio.run(main())
