from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Self
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models import Base
from src.settings.repository import SettingsRepository
from src.users.repository import UserRepository
from src.users.exceptions import UsernameOrEmailAlreadyExists


class UserSettingsUOW:
    __instance = None

    # def __new__(cls, *args, **kwargs) -> Self:
    #     if cls.__instance is None:
    #         cls.__instance = super().__new__(cls, *args, **kwargs)
    #     return cls.__instance

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
