from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.repository import UserRepository
from app.users.service import UserService


async def get_user_service(
    async_session: AsyncSession = Depends(get_async_session),
) -> UserService:
    repository = UserRepository(async_session)
    return UserService(repository=repository)
