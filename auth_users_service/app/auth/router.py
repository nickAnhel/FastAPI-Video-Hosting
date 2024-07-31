from fastapi import (
    APIRouter,
    Response,
    Depends,
)

from app.users.schemas import UserGet, UserGetWithPassword
from app.auth.schemas import Token
from app.auth.dependencies import authenticate_user, get_current_user_for_refresh, get_current_user
from app.auth.utils import create_access_token, create_refresh_token


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

    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return Token(
        access_token=access_token,
    )


@auth_router.post("/refresh", response_model_exclude_none=True)
async def refresh_jwt_token(
    user: UserGet = Depends(get_current_user_for_refresh),
) -> Token:
    access_token = create_access_token(user)

    return Token(
        access_token=access_token,
    )


@auth_router.post("/check")
async def check_token(
    user: UserGet = Depends(get_current_user),
) -> str:
    return str(user.id)
