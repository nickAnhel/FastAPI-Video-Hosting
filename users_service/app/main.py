from fastapi import FastAPI

from app.config import settings
from app.routes import get_routes


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/users/openapi.json",
    docs_url="/users/docs",
)


for route in get_routes():
    app.include_router(route)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
