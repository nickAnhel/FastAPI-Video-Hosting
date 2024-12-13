from sqladmin import Admin

from src.config import settings
from src.database import async_engine
from src.admin.auth import AdminAuth
from src.admin.views import (
    UserAdmin,
    SettingsAdmin,
    VideoAdmin,
    PlaylistAdmin,
    CommentAdmin,
    SessionAdmin,
)


def create_admin(app) -> Admin:
    authentication_backend = AdminAuth(secret_key=settings.admin_settings.admin_secret_key)  # type: ignore
    admin = Admin(app=app, engine=async_engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(SettingsAdmin)
    admin.add_view(VideoAdmin)
    admin.add_view(PlaylistAdmin)
    admin.add_view(CommentAdmin)
    admin.add_view(SessionAdmin)

    return admin
