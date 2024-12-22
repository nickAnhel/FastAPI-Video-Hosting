from fastapi import HTTPException, status
from fastapi.requests import Request


from src.settings.exceptions import (
    EmailNotVerified,
    TelegramNotVerified
)


async def email_not_verified_handler(request: Request, exc: EmailNotVerified) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(exc),
    )


async def telegram_not_verified_handler(
    request: Request, exc: TelegramNotVerified
) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail=str(exc),
    )
