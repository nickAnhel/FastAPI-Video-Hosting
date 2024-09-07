from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.users.schemas import UserGet
from app.settings.service import SettingsService
from app.settings.schemas import SettingsUpdate, SettingsGet
from app.settings.dependencies import get_settings_service


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
    return await service.udpate(user_id=user.id, data=data)
