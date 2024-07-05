from fastapi import APIRouter, UploadFile, HTTPException, Depends, Form, status

from app.client import S3Client
from app.dependencies import get_s3_client
from app.schemas import FileSchema


s3_router = APIRouter(
    prefix="/s3",
    tags=["S3 Storage"],
)


@s3_router.post("/")
async def upload_file(
    file: UploadFile,
    filename: str = Form(...),
    s3_client: S3Client = Depends(get_s3_client),
) -> FileSchema:
    try:
        await s3_client.upload_file(file.file, filename)  # type: ignore
        return FileSchema(filename=filename)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        ) from exc


@s3_router.delete("/")
async def delete_file(
    filename: str,
    s3_client: S3Client = Depends(get_s3_client),
) -> dict[str, str]:
    try:
        await s3_client.delete_file(filename)  # type: ignore
        return {
            "detail": "File deleted successfully",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file",
        ) from exc
