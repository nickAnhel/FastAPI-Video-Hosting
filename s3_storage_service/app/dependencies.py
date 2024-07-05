from app.client import S3Client
from app.config import settings


async def get_s3_client() -> S3Client:
    return S3Client(
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        bucket_name=settings.bucket_name,
        storage_url=settings.storage_url,
    )
