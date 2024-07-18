from fastapi import FastAPI

from app.config import settings
from app.comments.router import comment_router


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/comments/openapi.json",
    docs_url="/comments/docs",
)


app.include_router(comment_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
