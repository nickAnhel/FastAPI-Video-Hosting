import bcrypt
import aio_pika
from itsdangerous import URLSafeTimedSerializer

from src.config import settings
from src.schemas import Email

from src.users.exceptions import FailedToDecodeToken


def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def send_verification_email(message: Email) -> None:
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


serializer = URLSafeTimedSerializer(
    secret_key=settings.verification_settings.secret_key,
    salt=settings.verification_settings.salt,
)


def create_url_safe_token(data: dict[str, str]) -> str:
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str) -> dict[str, str]:
    try:
        token_data = serializer.loads(token)
        return token_data

    except Exception as exc:
        print(str(exc))
        raise FailedToDecodeToken(
            "Failed to decode email verification token"
        ) from exc
