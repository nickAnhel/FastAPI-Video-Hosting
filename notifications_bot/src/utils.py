from typing import Any
from itsdangerous import URLSafeTimedSerializer

from config import settings


serializer = URLSafeTimedSerializer(
    secret_key=settings.secret_key,
    salt=settings.salt,
)


def create_url_safe_token(data: dict[str, Any]) -> str:
    token = serializer.dumps(data)
    return token
