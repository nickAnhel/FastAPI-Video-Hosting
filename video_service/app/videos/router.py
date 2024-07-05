from fastapi import APIRouter


video_router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)
