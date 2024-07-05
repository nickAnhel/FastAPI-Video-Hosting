from contextlib import asynccontextmanager
from aiobotocore.session import get_session


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        storage_url: str,
    ) -> None:
        self._config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": storage_url,
        }
        self._bucket_name = bucket_name
        self._session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self._session.create_client("s3", **self._config) as client:
            yield client

    async def upload_file(
        self,
        file: bytes,
        filename: str,
    ) -> None:
        async with self.get_client() as client:  # type: ignore
            await client.put_object(  # type: ignore
                Bucket=self._bucket_name,
                Key=filename,
                Body=file,
            )

    async def delete_file(
        self,
        filename: str,
    ) -> None:
        async with self.get_client() as client:  # type: ignore
            await client.delete_object(  # type: ignore
                Bucket=self._bucket_name,
                Key=filename,
            )
