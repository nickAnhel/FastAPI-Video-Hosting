from fastapi import (
    APIRouter,
    Response,
    Depends,
)

from src.users.schemas import UserGet, UserGetWithPassword
from src.auth.schemas import Token
from src.auth.dependencies import authenticate_user, get_current_user_for_refresh, get_current_user
from src.auth.utils import create_access_token, create_refresh_token
from src.auth.config import auth_settings


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
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


@router.post("/refresh")
async def refresh_jwt_token(
    user: UserGet = Depends(get_current_user_for_refresh),
) -> Token:
    access_token = create_access_token(user)

    return Token(
        access_token=access_token,
    )


@router.post("/logout")
async def remove_refresh_token(
    response: Response,
) -> None:
    response.delete_cookie(key=auth_settings.refresh_token_cookie_key)


@router.post("/check")
async def check_token(
    user: UserGet = Depends(get_current_user),
) -> str:
    return str(user.id)
