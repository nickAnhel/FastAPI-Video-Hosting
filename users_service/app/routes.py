from fastapi import APIRouter


def get_routes() -> list[APIRouter]:
    from app.users.router import users_router
    return [
        users_router,
    ]
