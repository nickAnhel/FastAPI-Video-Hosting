from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.setup_app import register_routes, register_exception_handlers
from src.admin.admin import create_admin

app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/openapi.json",
    docs_url="/docs",
)
admin = create_admin(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_settings.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_routes(app)
register_exception_handlers(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
