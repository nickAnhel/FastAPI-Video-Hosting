import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.notifications.router import router


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/notifications/openapi.json",
    docs_url="/notifications/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
