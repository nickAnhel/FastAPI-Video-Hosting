from fastapi import APIRouter, Depends

from app.notifications.service import INotificationService
from app.notifications.schemas import (
    ConsoleNotification,
    EmailNotification,
    TelegramNotification,
)
from app.notifications.dependencies import (
    get_console_notification_service,
    get_email_notification_service,
    get_telegram_notification_service,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/console")
async def send_console_notification(
    data: ConsoleNotification,
    service: INotificationService[ConsoleNotification] = Depends(get_console_notification_service),
) -> dict[str, str]:
    service.send_notification(data)
    return {"detail": "Console notification sent"}


@router.post("/email")
async def send_email_notification(
    data: EmailNotification,
    service: INotificationService[EmailNotification] = Depends(get_email_notification_service),
) -> dict[str, str]:
    service.send_notification(data)
    return {"detail": "Email notification sent"}


@router.post("/telegram")
async def send_telegram_notification(
    data: TelegramNotification,
    service: INotificationService[TelegramNotification] = Depends(get_telegram_notification_service),
) -> dict[str, str]:
    service.send_notification(data)
    return {"detail": "Telegram notification sent"}
