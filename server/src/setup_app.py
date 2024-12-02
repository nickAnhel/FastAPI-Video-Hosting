from fastapi import FastAPI

# Routes
from src.users.router import router as users_router
from src.auth.router import router as auth_router
from src.settings.router import router as settings_router
from src.comments.router import router as comments_router
from src.playlists.router import router as playlists_router
from src.videos.router import router as videos_router

# Exception handlers
from src.exceptions import (
    PermissionDenied,
)
from src.exc_handlers import (
    permission_denied_handler,
)

from src.users.exc_handlers import (
    user_not_found_handler,
    username_or_email_already_exists_handler,
    user_not_in_subscriptions_handler,
    cant_subscribe_to_user_handler,
    cant_unsubscribe_from_user_handler,
    wrong_value_of_order_handler,
    wrong_limit_or_offset_handler,
)
from src.users.exceptions import (
    UserNotFound,
    UsernameOrEmailAlreadyExists,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
)

from src.comments.exc_handlers import (
    comment_not_found_handler,
    comment_content_wrong_format_handler,
)
from src.comments.exceptions import (
    CommentNotFound,
    CommentContentWrongFormat,
)

from src.playlists.exc_handlers import (
    playlist_not_found_handler,
    cant_remove_video_handler,
    cant_add_video_handler,
)
from src.playlists.exceptions import (
    PlaylistNotFound,
    CantRemoveVideoFromPlaylist,
    CantAddVideoToPlaylist,
)

from src.videos.exceptions import (
    VideoNotFound,
    VideoTitleAlreadyExists,
    VideoDataWrongFormat,
)
from src.videos.exc_handlers import (
    video_not_found_handler,
    video_title_already_exists_handler,
    video_data_wrong_format_handler,
)

from src.s3_storage.exceptions import (
    CantUploadFileToStorage,
    CantDeleteFileFromStorage,
)
from src.s3_storage.exc_handlers import (
    cant_upload_file_handler,
    cant_delete_file_handler,
)


def register_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(settings_router)
    app.include_router(videos_router)
    app.include_router(comments_router)
    app.include_router(playlists_router)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore

    app.add_exception_handler(UserNotFound, user_not_found_handler)  # type: ignore
    app.add_exception_handler(UsernameOrEmailAlreadyExists, username_or_email_already_exists_handler)  # type: ignore
    app.add_exception_handler(UserNotInSubscriptions, user_not_in_subscriptions_handler)  # type: ignore
    app.add_exception_handler(CantSubscribeToUser, cant_subscribe_to_user_handler)  # type: ignore
    app.add_exception_handler(CantUnsubscribeFromUser, cant_unsubscribe_from_user_handler)  # type: ignore
    app.add_exception_handler(WrongValueOfOrder, wrong_value_of_order_handler)  # type: ignore
    app.add_exception_handler(WrongLimitOrOffset, wrong_limit_or_offset_handler)  # type: ignore

    app.add_exception_handler(CommentNotFound, comment_not_found_handler)  # type: ignore
    app.add_exception_handler(CommentContentWrongFormat, comment_content_wrong_format_handler)  # type: ignore

    app.add_exception_handler(PlaylistNotFound, playlist_not_found_handler)  # type: ignore
    app.add_exception_handler(CantRemoveVideoFromPlaylist, cant_remove_video_handler)  # type: ignore
    app.add_exception_handler(CantAddVideoToPlaylist, cant_add_video_handler)  # type: ignore

    app.add_exception_handler(VideoNotFound, video_not_found_handler)  # type: ignore
    app.add_exception_handler(VideoTitleAlreadyExists, video_title_already_exists_handler)  # type: ignore
    app.add_exception_handler(VideoDataWrongFormat, video_data_wrong_format_handler)  # type: ignore

    app.add_exception_handler(CantUploadFileToStorage, cant_upload_file_handler)  # type: ignore
    app.add_exception_handler(CantDeleteFileFromStorage, cant_delete_file_handler)  # type: ignore
