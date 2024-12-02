from src.s3_storage.client import s3_client


async def upload_file(
    file: bytes,
    filename: str,
) -> bool:
    if not await s3_client.upload_file(file, filename):
        return False

    return True


async def delete_files(
    filenames: list[str],
) -> bool:
    for filename in filenames:
        if not await s3_client.delete_file(filename):
            return False

    return True
