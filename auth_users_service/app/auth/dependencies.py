from typing import Any, Callable, Coroutine
from fastapi import (
    HTTPException,
    Request,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.users.exceptions import UserNotFound
from app.auth.utils import validate_password, decode_jwt, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.users.schemas import UserGet, UserGetWithPassword, UserGetWithProfile


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithPassword:
    try:
        user: UserGetWithPassword = await user_service.get_user(
            include_password=True,
            username=form_data.username,
        )  # type: ignore
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
        ) from exc

    if not validate_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
        )

    return user


def _get_token_payload(
    token: str,
) -> dict[str, Any]:
    try:
        return decode_jwt(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc


def _get_token_payload_from_header(
    token: str = Depends(oauth2_scheme),
) -> dict[str, Any]:
    return _get_token_payload(token)


def _get_token_payload_from_cookie(
    request: Request,
) -> dict[str, Any]:
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing refresh token",
        )

    return _get_token_payload(token)


def _check_token_type(
    token_payload: dict[str, Any],
    token_type: str,
) -> None:
    if not token_payload.get("type") == token_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid token type: {token_payload.get('type')!r}",
        )


def get_current_user_closure(
    include_profile: bool = False,
    include_subscriptions: bool = False,
) -> Callable[..., Coroutine[Any, Any, UserGet | UserGetWithProfile]]:
    async def get_current_user_wrapper(
        token_payload: dict[str, Any] = Depends(_get_token_payload_from_header),
        user_service: UserService = Depends(get_user_service),
    ) -> UserGet | UserGetWithProfile:
        _check_token_type(token_payload, ACCESS_TOKEN_TYPE)

        try:
            return await user_service.get_user(
                include_profile=include_profile,
                include_subscriptions=include_subscriptions,
                id=token_payload.get("sub"),
            )  # type: ignore

        except UserNotFound as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token",
            ) from exc

    return get_current_user_wrapper


get_current_user = get_current_user_closure()
get_current_user_with_profile = get_current_user_closure(include_profile=True)
get_current_user_with_subscriptions = get_current_user_closure(include_subscriptions=True)


async def get_current_user_for_refresh(
    token_payload: dict[str, Any] = Depends(_get_token_payload_from_cookie),
    user_service: UserService = Depends(get_user_service),
) -> UserGet:
    _check_token_type(token_payload, REFRESH_TOKEN_TYPE)

    try:
        return await user_service.get_user(
            id=token_payload.get("sub"),
        )  # type: ignore

    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        ) from exc
