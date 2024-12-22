from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.users.schemas import UserGet
from src.settings.service import SettingsService
from src.settings.schemas import SettingsUpdate, SettingsGet
from src.settings.dependencies import get_settings_service


router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get("/")
async def get_user_settings(
    user: UserGet = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
) -> SettingsGet:
    return await service.get(user_id=user.id)


@router.put("/")
async def update_settings(
    data: SettingsUpdate,
    user: UserGet = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
) -> SettingsGet:
    return await service.udpate(user=user, data=data)
