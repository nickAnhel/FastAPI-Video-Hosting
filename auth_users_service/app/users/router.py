from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.exc import IntegrityError, CompileError, DBAPIError

from app.auth.dependencies import get_current_user, get_current_user_with_subscriptions
from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.users.schemas import UserCreate, UserGet, UserGetWithProfile, UserGetWithSubscriptions
from app.users.enums import UserOrder
from app.users.exceptions import (
    CantDeleteUsersVideos,
    UserNotFound,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
)


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.post("/")
async def create_user(
    data: UserCreate,
    users_service: UserService = Depends(get_user_service),
) -> UserGet:
    try:
        return await users_service.create_user(data)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from exc


@users_router.get("/me")
async def get_current_user_info(
    user: UserGetWithSubscriptions = Depends(get_current_user_with_subscriptions),
) -> UserGetWithSubscriptions:
    return user


@users_router.get("/list")
async def get_users(
    order: UserOrder = UserOrder.ID,
    offset: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> list[UserGet]:
    try:
        return await user_service.get_users(order=order, offset=offset, limit=limit)
    except CompileError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid value of order",
        ) from exc
    except DBAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Limit and offset must be positive integers or 0",
        ) from exc


@users_router.get("/")
async def get_user_by_id(
    id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithProfile:
    try:
        return await user_service.get_user(include_profile=True, id=id)  # type: ignore
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc


@users_router.delete("/")
async def delete_user(
    request: Request,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await user_service.delete_user(
            token=request.headers.get("Authorization").replace("Bearer ", ""),  # type: ignore
            id=user.id,
        )
        return {"detail": "User deleted successfully"}
    except CantDeleteUsersVideos as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Can't delete users videos",
        ) from exc


@users_router.post("/subscribe")
async def subscribe_to_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await user_service.subscribe(user_id=user_id, subscriber_id=user.id)
        return {"detail": "User subscribed successfully"}
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc
    except CantSubscribeToUser as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't subscribe to yourself",
        ) from exc


@users_router.delete("/unsubscribe")
async def unsubscribe_from_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    try:
        await user_service.unsubscribe(user_id=user_id, subscriber_id=user.id)
        return {"detail": "User unsubscribed successfully"}
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from exc
    except UserNotInSubscriptions as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id {user_id} not in subscriptions",
        ) from exc
    except CantUnsubscribeFromUser as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't unsubscribe from yourself",
        ) from exc
