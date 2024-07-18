from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, status

from app.comments.dependencies import get_comment_service, get_current_user_id
from app.comments.service import CommentService
from app.comments.schemas import CommentCreate, CommentGet
from app.comments.enums import CommentOrder
from app.comments.exceptions import CommentNotFound, PermissionDenied


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


@comment_router.get("/")
async def get_comments(
    video_id: UUID,
    order: CommentOrder = CommentOrder.ID,  # type: ignore
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
    try:
        await comment_service.delete_comment(comment_id=comment_id, user_id=user_id)
        return {"detail": "Comment deleted successfully"}
    except CommentNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        ) from exc
    except PermissionDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete this comment",
        ) from exc
