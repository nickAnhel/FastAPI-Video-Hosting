import aiohttp

from app.config import settings


async def upload_file_to_s3(file: bytes, filename: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.services.s3_storage_service}/s3/",
            data={"file": file, "filename": filename},
        ) as response:
            return response.status == 200


async def delete_file_from_s3(filename: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f"{settings.services.s3_storage_service}/s3/",
            params={"filename": filename},
        ) as response:
            return response.status == 200


async def get_s3_storage_url() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{settings.services.s3_storage_service}/s3/",
        ) as response:
            url = await response.text()
            return url.replace('"', "")
