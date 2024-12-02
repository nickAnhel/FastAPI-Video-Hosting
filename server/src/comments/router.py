from uuid import UUID
from fastapi import APIRouter, Depends

from src.schemas import Status

from src.auth.dependencies import get_current_user
from src.users.schemas import UserGet

from src.comments.dependencies import get_comment_service
from src.comments.service import CommentService
from src.comments.schemas import CommentCreate, CommentGet
from src.comments.enums import CommentOrder


router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post("/")
async def create_comment(
    data: CommentCreate,
    user: UserGet = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> CommentGet:
    return await comment_service.create_comment(data=data, user_id=user.id)


@router.get("/list")
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


@router.delete("/")
async def delete_comment(
    comment_id: UUID,
    user: UserGet = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
) -> Status:
    await comment_service.delete_comment(comment_id=comment_id, user_id=user.id)
    return Status(detail="Comment deleted successfully")
