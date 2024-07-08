import aiohttp

from app.config import settings
from app.auth.schemas import User
from app.auth.exceptions import UserNotFound


async def get_user_from_users_service(username: str) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.services.users_service_url}/users/auth/{username}",
        ) as response:
            if response.status != 200:
                raise UserNotFound(username)

            res = await response.json()
            return User(**res)
