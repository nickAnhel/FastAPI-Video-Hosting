from fastapi import HTTPException, Request, status

from src.exceptions import PermissionDenied


async def permission_denied_handler(request: Request, exc: PermissionDenied) -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=str(exc),
    )
