from uuid import UUID
import aiohttp

from app.config import settings
from app.videos.exceptions import CantGetUserID


async def upload_file_to_s3(file: bytes, filename: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.s3_storage_service_url}/s3/",
            data={"file": file, "filename": filename},
        ) as response:
            print(response.status)
            return response.status == 200


async def delete_files_from_s3(filenames: list[str]) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.s3_storage_service_url}/s3/",
            json={"filenames": filenames},
        ) as response:
            return response.status == 200


async def get_s3_storage_url() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.services.s3_storage_service_url}/s3/",
        ) as response:
            url = await response.text()
            return url.replace('"', "")


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


async def delete_all_video_comments(video_id: UUID, token: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.comments_service_url}/comments/list?video_id={video_id}",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            return response.status == 200
