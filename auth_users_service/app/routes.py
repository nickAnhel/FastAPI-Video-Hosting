from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from app.users.router import users_router
    from app.auth.router import auth_router

    return [
        users_router,
        auth_router,
    ]
