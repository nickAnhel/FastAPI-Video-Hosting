from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status

from src.schemas import Status
from src.auth.dependencies import get_current_user, get_current_optional_user, get_current_user_with_profile
from src.users.dependencies import get_user_service
from src.users.service import UserService
from src.users.schemas import UserCreate, UserUpdate, UserGet, UserGetWithProfile
from src.users.enums import UserOrder


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
    user: UserGetWithProfile = Depends(get_current_user_with_profile),
) -> UserGetWithProfile:
    return user


@router.get("/list")
async def get_users(
    order: UserOrder = UserOrder.ID,
    desc: bool = False,
    offset: int = 0,
    limit: int = 100,
    user: UserGet | None = Depends(get_current_optional_user),
    user_service: UserService = Depends(get_user_service),
) -> list[UserGet]:
    return await user_service.get_users(
        user=user,
        order=order,
        desc=desc,
        offset=offset,
        limit=limit,
    )


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
) -> Status:
    await user_service.delete_user(
        token=request.headers.get("Authorization").replace("Bearer ", ""),  # type: ignore
        user_id=user.id,
    )
    return Status(detail="User deleted successfully")


@router.post("/subscribe")
async def subscribe_to_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Status:
    await user_service.subscribe(user_id=user_id, subscriber_id=user.id)
    return Status(detail="User subscribed successfully")


@router.delete("/unsubscribe")
async def unsubscribe_from_user(
    user_id: UUID,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Status:
    await user_service.unsubscribe(user_id=user_id, subscriber_id=user.id)
    return Status(detail="User unsubscribed successfully")


@router.put("/")
async def update_user(
    data: UserUpdate,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserGetWithProfile:
    return await user_service.update_user(user_id=user.id, data=data)


@router.put("/photo")
async def update_profile_photo(
    photo: UploadFile,
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Status:
    if photo.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only jpeg or png files are allowed for profile photos",
        )

    await user_service.update_profile_photo(user_id=user.id, photo=photo.file)  # type: ignore
    return Status(detail="Profile photo updated successfully")


@router.delete("/photo")
async def delete_profile_photo(
    user: UserGet = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> Status:
    await user_service.delete_profile_photo(user_id=user.id)
    return Status(detail="Profile photo deleted successfully")
