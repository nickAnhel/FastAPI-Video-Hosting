from uuid import UUID
from fastapi import APIRouter, Depends

from src.schemas import Status

from src.auth.dependencies import get_current_user
from src.users.schemas import UserGet

from src.notifications.dependencies import get_notifications_service
from src.notifications.service import NotificationsService
from src.notifications.schemas import NotificationGet


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get("/")
async def get_notifications(
    offset: int = 0,
    limit: int = 100,
    user: UserGet = Depends(get_current_user),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> list[NotificationGet]:
    return await notifications_service.get_notifications(
        user=user,
        offset=offset,
        limit=limit,
    )


@router.get("/new")
async def get_new_notifications_count(
    user: UserGet = Depends(get_current_user),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> int:
    return await notifications_service.get_new_notifications_count(user=user)


@router.delete("/")
async def delete_notification(
    notification_id: UUID,
    user: UserGet = Depends(get_current_user),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> Status:
    await notifications_service.delete_notification(
        notification_id=notification_id,
        user=user,
    )

    return Status(detail="Notification deleted successfully")
