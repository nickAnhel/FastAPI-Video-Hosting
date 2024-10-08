import aiohttp

from app.config import settings
from app.playlists.exceptions import CantGetUserID


async def get_user_id_by_token(token: str | None) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.auth_users_service_url}/auth/check",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            if response.status != 200:
                raise CantGetUserID()
            token = await response.text()
            return token.replace('"', "")
