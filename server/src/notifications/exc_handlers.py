from fastapi import HTTPException, status
from fastapi.requests import Request

from src.notifications.exceptions import NotificationNotFound


async def notification_not_found_handler(request: Request, exc: NotificationNotFound) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )
