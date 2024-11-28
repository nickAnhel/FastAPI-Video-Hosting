import io
from uuid import UUID
from sqlalchemy.exc import NoResultFound, DBAPIError, CompileError, IntegrityError
from PIL import Image

from app.database import async_session_maker
from app.config import settings
from app.users.uow import UserSettingsUOW
from app.users.repository import UserRepository
from app.users.utils import get_password_hash
from app.users.external import delete_all_users_videos, upload_file_to_s3, delete_files_from_s3
from app.grpc_transport.playlist_stub import plylist_grpc_stub
from app.users.enums import UserOrder
from app.users.exceptions import (
    UserNotFound,
    CantDeleteUsersVideos,
    UsernameOrEmailAlreadyExists,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
    CantUploadFileToS3,
    CantDeleteFileFromS3,
)
from app.users.schemas import (
    UserCreate,
    UserUpdate,
    UserGet,
    UserGetWithProfile,
    UserGetWithPassword,
    UserGetWithSubscriptions,
    Playlist,
)


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository: UserRepository = repository
        self._uow = UserSettingsUOW(session_maker=async_session_maker)

    async def create_user(
        self,
        data: UserCreate,
    ) -> UserGetWithProfile:
        """Create new user."""
        user_data = data.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["social_links"] = [str(link) for link in user_data["social_links"]]

        async with self._uow.start() as uow:
            user = await uow.user_repo.create(data=user_data)
            await uow.refresh(user)
            await uow.settings_repo.create(user_id=user.id)  # type: ignore

        self._create_default_playlists(user.id)  # type: ignore

        return UserGetWithProfile.model_validate(user)

    def _create_default_playlists(
        self,
        user_id: UUID,
    ) -> None:
        plylist_grpc_stub.create(
            data=Playlist(
                user_id=user_id,  # type: ignore
                title="Watch History",
                private=True,
            )
        )
        plylist_grpc_stub.create(
            data=Playlist(
                user_id=user_id,  # type: ignore
                title="Liked Videos",
                private=True,
            )
        )
        plylist_grpc_stub.create(
            data=Playlist(
                user_id=user_id,  # type: ignore
                title="Disliked Videos",
                private=True,
            )
        )

    async def get_user(
        self,
        include_password: bool = False,
        include_profile: bool = False,
        include_subscriptions: bool = False,
        **filters,
    ) -> UserGet | UserGetWithProfile | UserGetWithPassword:
        """Get user by filters (username, email or id)."""
        try:
            user = await self._repository.get_single(**filters)
        except NoResultFound as exc:
            raise UserNotFound(f"User with filters {filters} not found") from exc

        if include_subscriptions:
            return UserGetWithSubscriptions.model_validate(user)

        if include_profile:
            return UserGetWithProfile.model_validate(user)

        if include_password:
            return UserGetWithPassword.model_validate(user)

        return UserGet.model_validate(user)

    async def get_users(
        self,
        user: UserGet | None = None,
        order: UserOrder = UserOrder.ID,
        desc: bool = False,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        """Get users with pagination and sorting."""
        try:
            users = await self._repository.get_multi(
                user_id=user.id if user else None,  # type: ignore
                order=order,
                order_desc=desc,
                offset=offset,
                limit=limit,
            )

            if user:
                users_pydantic: list[UserGet] = []

                for u in users:
                    if u.id == user.id:
                        continue

                    users_pydantic.append(
                        UserGet(
                            id=u.id,
                            username=u.username,
                            email=u.email,
                            subscribers_count=u.subscribers_count,
                            is_subscribed=(user.id in [s.id for s in u.subscribers]),
                        )
                    )

                return users_pydantic

            return [UserGet.model_validate(user) for user in users]

        except CompileError as exc:
            raise WrongValueOfOrder(f"Wrong value of order: {order}") from exc

        except DBAPIError as exc:
            raise WrongLimitOrOffset("Limit and offset must be positive integers or 0") from exc

    async def update_user(
        self,
        user_id: UUID,
        data: UserUpdate,
    ) -> UserGetWithProfile:
        """Update user by id."""
        try:
            user_data = data.model_dump(exclude_none=True)

            if "social_links" in user_data:
                user_data["social_links"] = [str(link) for link in user_data["social_links"]]

            user = await self._repository.update(
                data=user_data,
                id=user_id,
            )
            return UserGetWithProfile.model_validate(user)

        except NoResultFound as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc

        except IntegrityError as exc:
            raise UsernameOrEmailAlreadyExists(f"User with username {data.username} already exists") from exc

    async def _delete_all_files_from_storage(
        self,
        user_id: UUID,
    ) -> bool:
        return await delete_files_from_s3(
            filenames=[
                settings.file_prefixes.profile_photo_small + str(user_id),
                settings.file_prefixes.profile_photo_medium + str(user_id),
            ],
        )

    async def update_profile_photo(
        self,
        user_id: UUID,
        photo: bytes,
    ) -> bool:
        """Update user profile photo."""
        img_small = Image.open(photo)
        img_medium = Image.open(photo)

        img_small.thumbnail((80, 80))
        img_medium.thumbnail((160, 160))

        img_small_bytes = io.BytesIO()
        img_medium_bytes = io.BytesIO()

        img_small.save(img_small_bytes, "PNG")
        img_small_bytes = img_small_bytes.getvalue()

        img_medium.save(img_medium_bytes, "PNG")
        img_medium_bytes = img_medium_bytes.getvalue()

        await self._delete_all_files_from_storage(user_id)

        if not (
            await upload_file_to_s3(
                file=img_small_bytes,
                filename=settings.file_prefixes.profile_photo_small + str(user_id),
            )
            and await upload_file_to_s3(
                file=img_medium_bytes,
                filename=settings.file_prefixes.profile_photo_medium + str(user_id),
            )
        ):
            await self._delete_all_files_from_storage(user_id)
            raise CantUploadFileToS3("Failed to upload file to S3")

        return True

    async def delete_profile_photo(
        self,
        user_id: UUID,
    ) -> bool:
        """Delete user profile photo."""
        if not (await self._delete_all_files_from_storage(user_id)):
            raise CantDeleteFileFromS3("Failed to delete file from S3")

        return True

    async def delete_user(
        self,
        token: str,
        user_id: UUID,
    ) -> None:
        """Delete user by filters (username, email or id)."""
        if not await delete_files_from_s3(
            filenames=[settings.file_prefixes.profile_photo_small + str(user_id)],
        ):
            raise CantDeleteFileFromS3("Failed to delete file from S3")

        if not await delete_all_users_videos(token=token):
            raise CantDeleteUsersVideos()

        await self._repository.delete(id=user_id)

    async def subscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        """Subscribe to user."""
        if user_id == subscriber_id:
            raise CantSubscribeToUser("Can't subscribe to yourself")

        try:
            await self._repository.subscribe(user_id=user_id, subscriber_id=subscriber_id)
        except NoResultFound as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc

    async def unsubscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        """Unsubscribe from user."""
        if user_id == subscriber_id:
            raise CantUnsubscribeFromUser("Can't unsubscribe from yourself")

        try:
            await self._repository.unsubscribe(user_id=user_id, subscriber_id=subscriber_id)

        except NoResultFound as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc

        except ValueError as exc:
            raise UserNotInSubscriptions(
                f"User with id {subscriber_id} not found in subscribers of {user_id}"
            ) from exc
