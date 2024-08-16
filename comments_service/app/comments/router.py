from uuid import UUID
from fastapi import APIRouter, Depends

from app.comments.dependencies import get_comment_service, get_current_user_id
from app.comments.service import CommentService
from app.comments.schemas import CommentCreate, CommentGet
from app.comments.enums import CommentOrder


comment_router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@comment_router.post("/")
async def create_comment(
    data: CommentCreate,
    user_id: UUID = Depends(get_current_user_id),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentGet:
    return await comment_service.create_comment(data=data, user_id=user_id)


@comment_router.get("/list")
async def get_comments(
    video_id: UUID,
    order: CommentOrder = CommentOrder.ID,
    offset: int = 0,
    limit: int = 100,
    comment_service: CommentService = Depends(get_comment_service),
) -> list[CommentGet]:
    return await comment_service.get_comments(
        video_id=video_id,
        order=order,
        offset=offset,
        limit=limit,
    )


@comment_router.delete("/")
async def delete_comment(
    comment_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    comment_service: CommentService = Depends(get_comment_service),
) -> dict[str, str]:
    await comment_service.delete_comment(comment_id=comment_id, user_id=user_id)
    return {"detail": "Comment deleted successfully"}


@comment_router.delete("/list", dependencies=[Depends(get_current_user_id)])
async def delete_comments(
    video_id: UUID,
    comment_service: CommentService = Depends(get_comment_service),
) -> dict[str, str]:
    deleted_comments_count = await comment_service.delete_comments(video_id=video_id)
    return {"detail": f"Successfully deleted {deleted_comments_count} comments"}
