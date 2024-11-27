from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.videos.router import video_router
from app.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
    PermissionDenied,
    CantUploadVideoToS3,
    CantUploadPreviewToS3,
    CantDeleteVideoFromS3,
    CantDeleteComments,
)
from app.videos.exc_handlers import (
    video_not_found_handler,
    video_title_already_exists_handler,
    video_data_wrong_format_handler,
    permission_denied_handler,
    cant_upload_video_to_s3_handler,
    cant_upload_preview_to_s3_handler,
    cant_delete_video_from_s3_handler,
    cant_delete_comments_handler,
)


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/videos/openapi.json",
    docs_url="/videos/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost/", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router)

app.add_exception_handler(VideoNotFound, video_not_found_handler)  # type: ignore
app.add_exception_handler(VideoTitleAlreadyExists, video_title_already_exists_handler)  # type: ignore
app.add_exception_handler(VideoDataWrongFormat, video_data_wrong_format_handler)  # type: ignore
app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore
app.add_exception_handler(CantUploadVideoToS3, cant_upload_video_to_s3_handler)  # type: ignore
app.add_exception_handler(CantUploadPreviewToS3, cant_upload_preview_to_s3_handler)  # type: ignore
app.add_exception_handler(CantDeleteVideoFromS3, cant_delete_video_from_s3_handler)  # type: ignore
app.add_exception_handler(CantDeleteComments, cant_delete_comments_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
