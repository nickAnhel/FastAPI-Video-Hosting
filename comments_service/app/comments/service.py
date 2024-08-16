from uuid import UUID
from sqlalchemy.exc import DBAPIError

from app.comments.schemas import CommentCreate, CommentGet
from app.comments.repository import CommentRepository
from app.comments.enums import CommentOrder
from app.comments.exceptions import CommentNotFound, PermissionDenied, CommentContentWrongFormat
from app.comments.external import get_video_author_id


class CommentService:
    def __init__(self, repository: CommentRepository):
        self._repository = repository

    async def create_comment(
        self,
        data: CommentCreate,
        user_id: UUID,
    ) -> CommentGet:
        comment_data = data.model_dump()
        comment_data["user_id"] = user_id

        try:
            comment_model = await self._repository.create(data=comment_data)
        except DBAPIError as exc:
            raise CommentContentWrongFormat("Comment content is too long") from exc

        return CommentGet.model_validate(comment_model)

    async def get_comments(
        self,
        video_id: UUID,
        order: CommentOrder = CommentOrder.ID,  # type: ignore
        offset: int = 0,
        limit: int = 100,
    ) -> list[CommentGet]:
        comments = await self._repository.get_multi(
            order=order,
            offset=offset,
            limit=limit,
            video_id=video_id,
        )
        return [CommentGet.model_validate(comment) for comment in comments]

    async def delete_comment(
        self,
        comment_id: UUID,
        user_id: UUID,
    ) -> None:
        comment = await self._repository.get_single(id=comment_id)
        if not comment:
            raise CommentNotFound(f"Comment with id {comment_id} not found")

        video_author_id = await get_video_author_id(video_id=comment.video_id)
        if not user_id in (comment.user_id, video_author_id):
            raise PermissionDenied(f"User with id {user_id} can't delete comment with id {comment_id}")

        await self._repository.delete(id=comment_id)

    async def delete_comments(
        self,
        video_id: UUID,
    ) -> int:
        return await self._repository.delete(video_id=video_id)
