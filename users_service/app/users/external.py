from uuid import UUID
import aiohttp

from app.config import settings
from app.users.exceptions import InvalidAuthToken


async def get_user_id_from_auth_token(access_token: str) -> UUID:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.auth_service_url}/auth/check",
            headers={"Authorization": f"Bearer {access_token}"},
        ) as response:
            if response.status != 200:
                raise InvalidAuthToken()

            res = await response.text()
            return UUID(res.replace('"', ""))
