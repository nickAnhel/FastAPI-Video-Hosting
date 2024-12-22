from fastapi import HTTPException, status
from fastapi.requests import Request


from src.users.exceptions import (
    UserNotFound,
    UsernameOrEmailAlreadyExists,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
    FailedToDecodeToken,
)


async def user_not_found_handler(request: Request, exc: UserNotFound) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


async def username_or_email_already_exists_handler(
    request: Request, exc: UsernameOrEmailAlreadyExists
) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exc),
    )


async def user_not_in_subscriptions_handler(request: Request, exc: UserNotInSubscriptions) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def cant_subscribe_to_user_handler(request: Request, exc: CantSubscribeToUser) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def cant_unsubscribe_from_user_handler(request: Request, exc: CantUnsubscribeFromUser) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


async def wrong_value_of_order_handler(request: Request, exc: WrongValueOfOrder) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc),
    )


async def wrong_limit_or_offset_handler(request: Request, exc: WrongLimitOrOffset) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc),
    )

async def failed_to_docode_token_handler(request: Request, exc: FailedToDecodeToken) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
