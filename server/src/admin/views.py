from fastapi import Request
from sqladmin import ModelView
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.config import settings
from src.database import async_session_maker
from src.s3_storage.utils import delete_files
from src.users.models import UserModel
from src.settings.models import SettingsModel
from src.videos.models import VideoModel
from src.playlists.models import PlaylistModel
from src.comments.models import CommentModel

from src.admin.models import SessionModel


class UserAdmin(ModelView, model=UserModel):
    column_list = ["id", "username", "email", "is_active", "is_admin"]
    column_searchable_list = ["id", "username"]

    async def on_model_delete(self, model: UserModel, request: Request) -> None:
        if await delete_files(
            [
                settings.file_prefixes.profile_photo_small + str(model.id),
                settings.file_prefixes.profile_photo_medium + str(model.id),
                settings.file_prefixes.profile_photo_large + str(model.id),
            ]
        ):
            return await super().on_model_delete(model, request)


class SettingsAdmin(ModelView, model=SettingsModel):
    column_list = ["id", "user_id"]
    column_searchable_list = ["user_id"]


class VideoAdmin(ModelView, model=VideoModel):
    column_list = ["id", "user_id", "title", "views", "likes", "dislikes", "created_at"]
    column_searchable_list = ["title", "description"]
    column_sortable_list = ["views", "likes", "dislikes", "created_at"]

    async def on_model_delete(self, model: VideoModel, request: Request) -> None:
        if await delete_files(
            [
                settings.file_prefixes.video + str(model.id),
                settings.file_prefixes.preview + str(model.id),
            ]
        ):
            async with async_session_maker() as session:
                video_query = (
                    select(VideoModel)
                    .filter_by(id=model.id)
                    .options(selectinload(VideoModel.playlists))
                )

                res = await session.execute(video_query)
                video = res.scalar_one()

                update_videos_count_stmt = (
                    update(PlaylistModel)
                    .filter(
                        PlaylistModel.id.in_([p.id for p in video.playlists])
                    )
                    .values(videos_count=PlaylistModel.videos_count - 1)
                )

                await session.execute(update_videos_count_stmt)
                await session.commit()

            return await super().on_model_delete(model, request)


class PlaylistAdmin(ModelView, model=PlaylistModel):
    column_list = ["id", "user_id", "title", "private"]
    column_searchable_list = ["title"]


class CommentAdmin(ModelView, model=CommentModel):
    column_list = ["id", "user_id", "video_id", "content_ellipsis", "created_at"]
    column_sortable_list = ["created_at"]


class SessionAdmin(ModelView, model=SessionModel):
    column_list = ["session_id", "user_id", "issued_at", "expires_at"]
    column_sortable_list = ["issued_at", "expires_at"]
