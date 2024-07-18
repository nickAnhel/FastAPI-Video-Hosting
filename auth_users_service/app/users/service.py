from app.users.schemas import UserCreate, UserGet, UserGetWithProfile, UserGetWithPassword
from app.users.repository import UserRepository
from app.users.exceptions import UserNotFound, CantDeleteUsersVideos
from app.users.utils import get_password_hash
from app.users.external import delete_all_users_videos


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
        **filters,
    ) -> UserGet | UserGetWithProfile | UserGetWithPassword:
        """Get user by filters (username, email or id)."""
        user = await self.repository.get_single(**filters)

        if not user:
            raise UserNotFound(f"User with filters {filters} not found")

        if include_profile:
            return UserGetWithProfile.model_validate(user)

        if include_password:
            return UserGetWithPassword.model_validate(user)

        return UserGet.model_validate(user)

    async def get_users(
        self,
        order: str = "id",
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        """Get users with pagination."""
        users = await self.repository.get_multiple(
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
