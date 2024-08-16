from fastapi import FastAPI

from app.config import settings
from app.comments.router import comment_router
from app.comments.exc_handlers import (
    comment_not_found_handler,
    permission_denied_handler,
    comment_content_wrong_format_handler,
)
from app.comments.exceptions import (
    CommentNotFound,
    PermissionDenied,
    CommentContentWrongFormat,
)


app = FastAPI(
    title=settings.project_title,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    openapi_url="/comments/openapi.json",
    docs_url="/comments/docs",
)


app.include_router(comment_router)

app.add_exception_handler(CommentNotFound, comment_not_found_handler)  # type: ignore
app.add_exception_handler(PermissionDenied, permission_denied_handler)  # type: ignore
app.add_exception_handler(CommentContentWrongFormat, comment_content_wrong_format_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
