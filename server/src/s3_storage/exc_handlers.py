from fastapi import HTTPException, status
from fastapi.requests import Request

from src.s3_storage.exceptions import CantUploadFileToStorage, CantDeleteFileFromStorage


async def cant_upload_file_handler(request: Request, exc: CantUploadFileToStorage) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )


async def cant_delete_file_handler(request: Request, exc: CantDeleteFileFromStorage) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(exc),
    )
