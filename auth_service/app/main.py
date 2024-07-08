from fastapi import FastAPI

from app.config import settings
from app.auth.router import auth_router


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/auth/openapi.json",
    docs_url="/auth/docs",
)


app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
