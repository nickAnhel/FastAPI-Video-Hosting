from uuid import UUID

from app.users.repository import UserRepository
from app.users.exceptions import UserNotFound, CantDeleteUsersVideos, UserNotInSubscriptions
from app.users.utils import get_password_hash
from app.users.external import delete_all_users_videos
from app.users.enums import UserOrder
from app.users.schemas import (
    UserCreate,
    UserGet,
    UserGetWithProfile,
    UserGetWithPassword,
    UserGetWithSubscriptions,
)
from app.users.models import UserModel


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository: UserRepository = repository

    async def create_user(self, data: UserCreate) -> UserGet:
        """Create new user."""
        user_data = data.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["social_links"] = [str(link) for link in user_data["social_links"]]

        user = await self.repository.create(data=user_data)
        return UserGet.model_validate(user)

    async def get_user(
        self,
        include_password: bool = False,
        include_profile: bool = False,
        include_subscriptions: bool = False,
        **filters,
    ) -> UserGet | UserGetWithProfile | UserGetWithPassword:
        """Get user by filters (username, email or id)."""
        user = await self.repository.get_single(**filters)

        if not user:
            raise UserNotFound(f"User with filters {filters} not found")

        if include_subscriptions:
            # user_subribers = [UserGet.model_validate(sub) for sub in user.subscribers]
            # user_subribed = [UserGet.model_validate(sub) for sub in user.subscribed]
            # user = UserGetWithProfile.model_validate(user)
            # return UserGetWithSubscriptions(
            #     **user.model_dump(),
            #     subscribers=user_subribers,
            #     subscribed=user_subribed,
            # )
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
        """Get users with pagination."""
        users: list[UserModel] = await self.repository.get_multiple(
            order=order,
            offset=offset,
            limit=limit,
        )
        return [UserGet.model_validate(user) for user in users]

    async def delete_user(
        self,
        token: str,
        **filters,
    ) -> None:
        """Delete user by filters (username, email or id)."""
        if not await delete_all_users_videos(token=token):
            raise CantDeleteUsersVideos()

        await self.repository.delete(**filters)

    async def subscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        """Subscribe to user."""
        try:
            await self.repository.subscribe(user_id=user_id, subscriber_id=subscriber_id)
        except AttributeError as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc

    async def unsubscribe(
        self,
        user_id: UUID,
        subscriber_id: UUID,
    ) -> None:
        """Unsubscribe from user."""
        try:
            await self.repository.unsubscribe(user_id=user_id, subscriber_id=subscriber_id)
        except AttributeError as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc
        except ValueError as exc:
            raise UserNotInSubscriptions(f"User with id {subscriber_id} not found in subscribers of {user_id}") from exc
