from uuid import UUID
import aiohttp

from app.config import settings
from app.comments.exceptions import CantGetUserID


async def get_user_id_by_token(token: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.auth_users_service_url}/auth/check",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            if response.status != 200:
                raise CantGetUserID()
            token = await response.text()
            return token.replace('"', "")


async def get_video_author_id(video_id: UUID) -> UUID:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.services.videos_service_url}/videos?video={video_id}",
        ) as response:
            video = await response.json()
            print(video)
            return UUID(video["user_id"])
