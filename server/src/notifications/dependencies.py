from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.notifications.service import NotificationsService
from src.notifications.repository import NotificationsRepository


def get_notifications_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> NotificationsService:
    notifications_repository = NotificationsRepository(async_session)
    return NotificationsService(notifications_repository)
