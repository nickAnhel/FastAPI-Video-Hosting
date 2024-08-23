from fastapi import (
    APIRouter,
    Response,
    Depends,
)

from app.users.schemas import UserGet, UserGetWithPassword
from app.auth.schemas import Token
from app.auth.dependencies import authenticate_user, get_current_user_for_refresh, get_current_user
from app.auth.utils import create_access_token, create_refresh_token
from app.auth.config import auth_settings


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/token")
async def get_jwt_token(
    response: Response,
    user: UserGetWithPassword = Depends(authenticate_user),
) -> Token:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie(
        key=auth_settings.refresh_token_cookie_key,
        value=refresh_token,
        max_age=auth_settings.refresh_token_expire_minutes,
        httponly=True,
    )

    return Token(
        access_token=access_token,
    )


@auth_router.post("/refresh")
async def refresh_jwt_token(
    user: UserGet = Depends(get_current_user_for_refresh),
) -> Token:
    access_token = create_access_token(user)

    return Token(
        access_token=access_token,
    )


@auth_router.post("/logout")
async def remove_refresh_token(
    response: Response,
) -> None:
    response.delete_cookie(key=auth_settings.refresh_token_cookie_key)


@auth_router.post("/check")
async def check_token(
    user: UserGet = Depends(get_current_user),
) -> str:
    return str(user.id)
