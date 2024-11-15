from uuid import UUID
from fastapi import APIRouter, Depends, Request

from app.auth.dependencies import get_current_user, get_current_user_with_subscriptions
from app.users.dependencies import get_user_service
from app.users.service import UserService
from app.users.schemas import UserCreate, UserUpdate, UserGet, UserGetWithProfile, UserGetWithSubscriptions
from app.users.enums import UserOrder


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/")
async def create_user(
    data: UserCreate,
    users_service: UserService = Depends(get_user_service),
) -> UserGetWithProfile:
    return await users_service.create_user(data)


@router.get("/me")
async def get_current_user_info(
    user: UserGetWithSubscriptions = Depends(get_current_user_with_subscriptions),
) -> UserGetWithSubscriptions:
    return user


@router.get("/list")
async def get_users(
    order: UserOrder = UserOrder.ID,
    offset: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> list[UserGet]:
    return await user_service.get_users(order=order, offset=offset, limit=limit)


@router.get("/")
async def get_user_by_id(
    id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithProfile:
    return await user_service.get_user(include_profile=True, id=id)  # type: ignore


@router.delete("/")
async def delete_user(
    request: Request,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    await user_service.delete_user(
        token=request.headers.get("Authorization").replace("Bearer ", ""),  # type: ignore
        id=user.id,
    )
    return {"detail": "User deleted successfully"}


@router.post("/subscribe")
async def subscribe_to_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    await user_service.subscribe(user_id=user_id, subscriber_id=user.id)
    return {"detail": "User subscribed successfully"}


@router.delete("/unsubscribe")
async def unsubscribe_from_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> dict[str, str]:
    await user_service.unsubscribe(user_id=user_id, subscriber_id=user.id)
    return {"detail": "User unsubscribed successfully"}


@router.put("/")
async def update_user(
    data: UserUpdate,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithProfile:
    return await user_service.update_user(user_id=user.id, data=data)
