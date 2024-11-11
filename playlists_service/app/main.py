import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.playlists.router import playlists_router
from app.grpc_transport.server import GRPCServer
from app.playlists.exc_handlers import (
    playlist_not_found_handler,
    permission_denied_handler,
    playlist_title_already_exists_handler,
    playlist_not_contain_video_handler,
)
from app.playlists.exceptions import (
    PlaylistNotFound,
    PermissionDenied,
    PlaylistTitleAlreadyExists,
    PlaylistDoesNotContainVideo,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    grpc_task = asyncio.create_task(GRPCServer().start())
    # await GRPCServer().start()
    try:
        yield
    finally:
        grpc_task.cancel()


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/playlists/openapi.json",
    docs_url="/playlists/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(playlists_router)

app.add_exception_handler(PlaylistNotFound, playlist_not_found_handler)  # type: ignore
app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore
app.add_exception_handler(PlaylistTitleAlreadyExists, playlist_title_already_exists_handler)  # type: ignore
app.add_exception_handler(PlaylistDoesNotContainVideo, playlist_not_contain_video_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
