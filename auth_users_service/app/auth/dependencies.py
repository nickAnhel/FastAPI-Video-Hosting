from typing import Any, Callable, Coroutine
from fastapi import (
    HTTPException,
    Depends,
    Form,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.users.exceptions import UserNotFound
from app.auth.utils import validate_password, decode_jwt, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.users.schemas import UserGet, UserGetWithPassword, UserGetWithProfile


http_bearer = HTTPBearer()


async def authenticate_user(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithPassword:
    try:
        user: UserGetWithPassword = await user_service.get_user(
            include_password=True,
            username=username,
        )  # type: ignore
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username",
        ) from exc

    if not validate_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect password",
        )

    return user


async def _get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict[str, Any]:
    token = credentials.credentials
    try:
        return decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


def get_current_user_closure(
    token_type: str,
    include_profile: bool = False,
) -> Callable[..., Coroutine[Any, Any, UserGet | UserGetWithProfile]]:
    async def get_current_user_by_token_type_wrapper(
        token_payload: dict[str, Any] = Depends(_get_token_payload),
        user_service: UserService = Depends(get_user_service),
    ) -> UserGet:
        given_token_type = token_payload.get("type")
        if given_token_type != token_type:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invalid token type {given_token_type!r}, expected {token_type!r}",
            )

        try:
            user = await user_service.get_user(
                include_profile=include_profile,
                id=token_payload.get("sub"),
            )  # type: ignore
        except UserNotFound as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
            ) from exc

        return user

    return get_current_user_by_token_type_wrapper


get_current_user = get_current_user_closure(ACCESS_TOKEN_TYPE)
get_current_user_with_profile = get_current_user_closure(ACCESS_TOKEN_TYPE, include_profile=True)
get_current_user_for_refresh = get_current_user_closure(REFRESH_TOKEN_TYPE)
