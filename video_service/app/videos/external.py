import aiohttp

from app.config import settings
from app.videos.exceptions import CantGetUserID

async def upload_file_to_s3(file: bytes, filename: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.s3_storage_service}/s3/",
            data={"file": file, "filename": filename},
        ) as response:
            print(response.status)
            return response.status == 200


async def delete_file_from_s3(filenames: list[str]) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.s3_storage_service}/s3/",
            json={"filenames": filenames},
        ) as response:
            return response.status == 200


async def get_s3_storage_url() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.services.s3_storage_service}/s3/",
        ) as response:
            url = await response.text()
            return url.replace('"', "")



async def get_user_id_by_token(token: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.auth_users_storage_service}/auth/check",
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            if response.status !=  200:
                raise CantGetUserID()
            token = await response.text()
            return token.replace('"', "")
