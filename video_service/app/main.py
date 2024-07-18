from fastapi import FastAPI

from app.config import settings
from app.videos.router import video_router


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/videos/openapi.json",
    docs_url="/videos/docs",
)


app.include_router(video_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
