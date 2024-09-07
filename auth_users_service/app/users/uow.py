from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Self
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models import Base
from app.settings.repository import SettingsRepository
from app.users.repository import UserRepository
from app.users.exceptions import UsernameOrEmailAlreadyExists


class UserSettingsUOW:
    def __init__(
        self,
        session_maker,
    ) -> None:
        self._session_maker = session_maker
        self._session: AsyncSession = None  # type: ignore

    @property
    def user_repo(self) -> UserRepository:
        return UserRepository(self._session)

    @property
    def settings_repo(self) -> SettingsRepository:
        return SettingsRepository(self._session)

    @asynccontextmanager
    async def start(self) -> AsyncGenerator[Self, Any]:
        self._session = self._session_maker()

        try:
            yield self
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise UsernameOrEmailAlreadyExists("Username or email already exists") from exc
        finally:
            await self._session.close()
            self._session = None  # type: ignore

    async def refresh(self, instance: Base) -> None:
        await self._session.flush()
        await self._session.refresh(instance)
