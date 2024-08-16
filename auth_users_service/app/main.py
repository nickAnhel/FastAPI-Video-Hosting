from fastapi import FastAPI

from app.config import settings
from app.routes import get_routes
from app.users.exc_handlers import (
    user_not_found_handler,
    username_or_email_already_exists_handler,
    user_not_in_subscriptions_handler,
    cant_delete_users_videos_handler,
    cant_subscribe_to_user_handler,
    cant_unsubscribe_from_user_handler,
    wrong_value_of_order_handler,
    wrong_limit_or_offset_handler,
)
from app.users.exceptions import (
    UserNotFound,
    UsernameOrEmailAlreadyExists,
    UserNotInSubscriptions,
    CantDeleteUsersVideos,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
)

app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/users/openapi.json",
    docs_url="/users/docs",
)


for route in get_routes():
    app.include_router(route)


app.add_exception_handler(UserNotFound, user_not_found_handler)  # type: ignore
app.add_exception_handler(UsernameOrEmailAlreadyExists, username_or_email_already_exists_handler)  # type: ignore
app.add_exception_handler(UserNotInSubscriptions, user_not_in_subscriptions_handler)  # type: ignore
app.add_exception_handler(CantDeleteUsersVideos, cant_delete_users_videos_handler)  # type: ignore
app.add_exception_handler(CantSubscribeToUser, cant_subscribe_to_user_handler)  # type: ignore
app.add_exception_handler(CantUnsubscribeFromUser, cant_unsubscribe_from_user_handler)  # type: ignore
app.add_exception_handler(WrongValueOfOrder, wrong_value_of_order_handler)  # type: ignore
app.add_exception_handler(WrongLimitOrOffset, wrong_limit_or_offset_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
