from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from app.users.router import router as users_router
    from app.auth.router import router as auth_router
    from app.settings.router import router as settings_router

    return [
        users_router,
        auth_router,
        settings_router,
    ]
