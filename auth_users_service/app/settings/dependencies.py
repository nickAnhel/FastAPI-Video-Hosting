from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.settings.service import SettingsService
from app.settings.repository import SettingsRepository


def get_settings_service(
    session: AsyncSession = Depends(get_async_session),
) -> SettingsService:
    return SettingsService(
        repository=SettingsRepository(session),
    )
