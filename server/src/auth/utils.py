from typing import Any
import datetime
import jwt
import bcrypt

from src.users.schemas import UserGet
from src.auth.config import auth_settings


TOKEN_TYPE_FIELD: str = "type"
ACCESS_TOKEN_TYPE: str = "access"
REFRESH_TOKEN_TYPE: str = "refresh"


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = auth_settings.private_key_path.read_text(),
    algorithm: str = auth_settings.algorithm,
    expire_minutes: int = auth_settings.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.UTC)

    to_encode.update(
        iat=now,
        exp=now + datetime.timedelta(minutes=expire_minutes),
    )

    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )


def decode_jwt(
    token: str,
    public_key: str = auth_settings.public_key_path.read_text(),
    algorithm: str = auth_settings.algorithm,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )


def create_token(
    token_type: str,
    payload: dict[str, Any],
    expire_minutes: int = auth_settings.access_token_expire_minutes,
) -> str:
    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type,
        **payload,
    }
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
    )


def create_access_token(user: UserGet) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
    }

    return create_token(
        token_type=ACCESS_TOKEN_TYPE,
        payload=payload,
        expire_minutes=auth_settings.access_token_expire_minutes,
    )


def create_refresh_token(user: UserGet) -> str:
    payload = {
        "sub": str(user.id),
        "username": user.username,
    }

    return create_token(
        token_type=REFRESH_TOKEN_TYPE,
        payload=payload,
        expire_minutes=auth_settings.refresh_token_expire_minutes,
    )
