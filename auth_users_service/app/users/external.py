import aiohttp

from app.config import settings


async def delete_all_users_videos(token: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.videos_service_url}/videos/list", headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return response.status == 200


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
