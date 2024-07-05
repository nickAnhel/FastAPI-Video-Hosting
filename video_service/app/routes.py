from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from app.videos.router import video_router

    return [
        video_router,
    ]
