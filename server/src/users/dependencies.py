from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.repository import UserRepository
from src.users.service import UserService


async def get_user_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> UserService:
    repository = UserRepository(async_session)
    return UserService(repository=repository)
