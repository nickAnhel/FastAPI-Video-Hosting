from sqlalchemy import select

from database import async_session_maker
from models import UserModel


async def get_user(telegram_username: str) -> UserModel:
    async with async_session_maker() as session:
        query = (
            select(UserModel)
            .filter_by(telegram_username=telegram_username)
        )

        res = await session.execute(query)
        return res.scalar_one()
