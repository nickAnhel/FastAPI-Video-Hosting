from fastapi import APIRouter


comment_router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@comment_router.get("/")
async def get_comments():
    return []
