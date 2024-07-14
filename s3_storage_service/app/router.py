from fastapi import APIRouter, UploadFile, HTTPException, Depends, Form, status

from app.client import S3Client
from app.dependencies import get_s3_client
from app.schemas import FilenameSchema, FilenamesSchema
from app.config import settings

s3_router = APIRouter(
    prefix="/s3",
    tags=["S3 Storage"],
)


@s3_router.post("/")
async def upload_file(
    file: UploadFile,
    filename: str = Form(...),
    s3_client: S3Client = Depends(get_s3_client),
) -> FilenameSchema:
    if not await s3_client.upload_file(file.file, filename):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        )

    return FilenameSchema(filename=filename)


@s3_router.delete("/")
async def delete_file(
    filenames: FilenamesSchema,
    s3_client: S3Client = Depends(get_s3_client),
) -> dict[str, str]:
    for filename in filenames.filenames:
        if not await s3_client.delete_file(filename):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file {filename}",
            )

    return {
        "detail": "Files deleted successfully",
    }


@s3_router.get("/")
async def get_storage_url() -> str:
    return settings.storage_url  # type: ignore
