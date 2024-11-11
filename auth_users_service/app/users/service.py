from uuid import UUID
from sqlalchemy.exc import NoResultFound, DBAPIError, CompileError

from app.database import async_session_maker
from app.users.uow import UserSettingsUOW
from app.users.repository import UserRepository
from app.users.utils import get_password_hash
from app.users.external import delete_all_users_videos
from app.grpc_transport.playlist_stub import plylist_grpc_stub
from app.users.enums import UserOrder
from app.users.exceptions import (
    UserNotFound,
    CantDeleteUsersVideos,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
)
from app.users.schemas import (
    UserCreate,
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
        order: UserOrder = UserOrder.ID,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        """Get users with pagination and sorting."""
        try:
            users = await self._repository.get_multiple(
                order=order,
                offset=offset,
                limit=limit,
            )
            return [UserGet.model_validate(user) for user in users]

        except CompileError as exc:
            raise WrongValueOfOrder(f"Wrong value of order: {order}") from exc

        except DBAPIError as exc:
            raise WrongLimitOrOffset("Limit and offset must be positive integers or 0") from exc

    async def delete_user(
        self,
        token: str,
        **filters,
    ) -> None:
        """Delete user by filters (username, email or id)."""
        if not await delete_all_users_videos(token=token):
            raise CantDeleteUsersVideos()

        await self._repository.delete(**filters)

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
