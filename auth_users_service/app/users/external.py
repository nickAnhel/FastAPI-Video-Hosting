import aiohttp

from app.config import settings


async def delete_all_users_videos(token: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.videos_service_url}/videos/list", headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return response.status == 200
