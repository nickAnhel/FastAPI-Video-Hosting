from fastapi import FastAPI

from app.config import settings
from app.playlists.router import playlists_router
from app.playlists.exc_handlers import playlist_not_found_handler, permission_denied_handler
from app.playlists.exceptions import PlaylistNotFound, PermissionDenied


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/playlists/openapi.json",
    docs_url="/playlists/docs",
)


app.include_router(playlists_router)

app.add_exception_handler(PlaylistNotFound, playlist_not_found_handler)  # type: ignore
app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
