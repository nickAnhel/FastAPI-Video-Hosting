import io
from pathlib import Path
from uuid import UUID
from sqlalchemy.exc import NoResultFound, DBAPIError, CompileError, IntegrityError
from PIL import Image
from jinja2 import Template

from src.config import settings
from src.database import async_session_maker
from src.schemas import Email

from src.s3_storage.utils import upload_file, delete_files
from src.s3_storage.exceptions import (
    CantUploadFileToStorage,
    CantDeleteFileFromStorage,
)

from src.settings.schemas import SettingsUpdate

from src.users.uow import UserSettingsUOW
from src.users.repository import UserRepository
from src.users.enums import UserOrder
from src.users.utils import (
    get_password_hash,
    send_verification_email,
    create_url_safe_token,
    decode_url_safe_token,
)
from src.users.exceptions import (
    UserNotFound,
    UsernameOrEmailAlreadyExists,
    UserNotInSubscriptions,
    CantSubscribeToUser,
    CantUnsubscribeFromUser,
    WrongValueOfOrder,
    WrongLimitOrOffset,
)
from src.users.schemas import (
    UserCreate,
    UserUpdate,
    UserGet,
    UserGetWithProfile,
    UserGetWithPassword,
    UserGetWithSubscriptions,
)


BASE_DIR = Path(__file__).parent.parent.parent


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

        user_data = UserGetWithProfile.model_validate(user)

        await self.send_email_verification(user=user_data)

        return user_data

    async def send_email_verification(
        self,
        user: UserGet,
    ) -> None:
        verify_token = create_url_safe_token(data={"email": user.email})
        verify_link = f"{settings.url_settings.backend_host}/users/email/verify/{verify_token}"

        with open(BASE_DIR / "templates" / "verify.html", "r", encoding="utf-8") as file:
            template = Template(file.read())

        email_body = template.render(verify_link=verify_link)
        message = Email(
            email=user.email,
            subject="ТипоTube Verify email",
            content=email_body,
        )

        await send_verification_email(message)

    async def verify_email(
        self,
        token: str,
    ) -> None:
        token_data = decode_url_safe_token(token)
        email = token_data.get("email")

        try:
            await self._repository.update(
                data={"is_verified_email": True},
                email=email,
            )
        except NoResultFound as exc:
            raise UserNotFound(f"User with email {email} not found") from exc

    async def verify_telegram(
        self,
        token: str,
    ) -> None:
        token_data = decode_url_safe_token(token)
        telegram_username = token_data.get("telegram_username")
        chat_id = int(token_data.get("chat_id"))  # type: ignore

        try:
            await self._repository.update(
                data={
                    "is_verified_telegram": True,
                    "telegram_chat_id": chat_id,
                },
                telegram_username=telegram_username,
            )
        except NoResultFound as exc:
            raise UserNotFound(f"User with telegram {telegram_username!r} not found") from exc

    async def get_user(
        self,
        curr_user: UserGet | None = None,
        include_password: bool = False,
        include_profile: bool = False,
        include_subscriptions: bool = False,
        **filters,
    ) -> UserGet | UserGetWithProfile | UserGetWithPassword:
        """Get user by filters (username, email or id)."""
        try:
            user = await self._repository.get_single(**filters)

            if curr_user:
                return UserGetWithProfile(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    telegram_username=user.telegram_username,
                    is_verified_email=user.is_verified_email,
                    is_verified_telegram=user.is_verified_telegram,
                    subscribers_count=user.subscribers_count,
                    about=user.about,
                    social_links=user.social_links,
                    is_subscribed=(curr_user.id in [u.id for u in user.subscribers]),
                )

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
                            telegram_username=u.telegram_username,
                            is_verified_email=u.is_verified_email,
                            is_verified_telegram=u.is_verified_telegram,
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

    async def search_users(
        self,
        query: str,
        user: UserGet | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        try:
            users = await self._repository.search(
                search_query=query,
                user_id=user.id if user else None,  # type: ignore
                offset=offset,
                limit=limit,
            )
            
            if user:
                users_pydantic: list[UserGet] = []

                for u in users:
                    users_pydantic.append(
                        UserGet(
                            id=u.id,
                            username=u.username,
                            email=u.email,
                            telegram_username=u.telegram_username,
                            is_verified_email=u.is_verified_email,
                            is_verified_telegram=u.is_verified_telegram,
                            subscribers_count=u.subscribers_count,
                            is_subscribed=(user.id in [s.id for s in u.subscribers]),
                        )
                    )

                return users_pydantic

            return [UserGet.model_validate(user) for user in users]

        except DBAPIError as exc:
            raise WrongLimitOrOffset("Limit and offset must be positive integers or 0") from exc

    async def update_user(
        self,
        curr_user: UserGet,
        data: UserUpdate,
    ) -> UserGetWithProfile:
        """Update user by id."""
        try:
            user_data = data.model_dump()

            if "social_links" in user_data:
                user_data["social_links"] = [str(link) for link in user_data["social_links"]]

            if user_data["telegram_username"] != curr_user.telegram_username:
                user_data["is_verified_telegram"] = False

                async with self._uow.start() as uow:
                    await uow.settings_repo.update(SettingsUpdate(enable_telegram_notifications=False), user_id=curr_user.id)
                    user = await uow.user_repo.update(
                        data=user_data,
                        id=curr_user.id,
                    )
                    return UserGetWithProfile.model_validate(user)

            user = await self._repository.update(
                data=user_data,
                id=curr_user.id,
            )
            return UserGetWithProfile.model_validate(user)

        except NoResultFound as exc:
            raise UserNotFound(f"User with id {curr_user.id} not found") from exc

        except IntegrityError as exc:
            raise UsernameOrEmailAlreadyExists(f"User with username {data.username} already exists") from exc

    async def _delete_all_files_from_storage(
        self,
        user_id: UUID,
    ) -> bool:
        return await delete_files(
            filenames=[
                settings.file_prefixes.profile_photo_small + str(user_id),
                settings.file_prefixes.profile_photo_medium + str(user_id),
                settings.file_prefixes.profile_photo_large + str(user_id),
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
        img_large = Image.open(photo)

        img_small.thumbnail((80, 80))
        img_medium.thumbnail((160, 160))
        img_large.thumbnail((240, 240))

        img_small_bytes = io.BytesIO()
        img_medium_bytes = io.BytesIO()
        img_large_bytes = io.BytesIO()

        img_small.save(img_small_bytes, "PNG")
        img_small_bytes = img_small_bytes.getvalue()

        img_medium.save(img_medium_bytes, "PNG")
        img_medium_bytes = img_medium_bytes.getvalue()

        img_large.save(img_large_bytes, "PNG")
        img_large_bytes = img_large_bytes.getvalue()

        await self._delete_all_files_from_storage(user_id)

        if not (
            await upload_file(
                file=img_small_bytes,
                filename=settings.file_prefixes.profile_photo_small + str(user_id),
            )
            and await upload_file(
                file=img_medium_bytes,
                filename=settings.file_prefixes.profile_photo_medium + str(user_id),
            )
            and await upload_file(
                file=img_large_bytes,
                filename=settings.file_prefixes.profile_photo_large + str(user_id),
            )
        ):
            await self._delete_all_files_from_storage(user_id)
            raise CantUploadFileToStorage()

        return True

    async def delete_profile_photo(
        self,
        user_id: UUID,
    ) -> bool:
        """Delete user profile photo."""
        if not await self._delete_all_files_from_storage(user_id):
            raise CantDeleteFileFromStorage()

        return True

    async def delete_user(
        self,
        user_id: UUID,
    ) -> None:
        """Delete user by filters (username, email or id)."""
        if not await self._delete_all_files_from_storage(user_id=user_id):
            raise CantDeleteFileFromStorage("Failed to delete file from S3")

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

    async def get_subscriptions(
        self,
        user_id: UUID,
        curr_user: UserGet | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[UserGet]:
        try:
            users = await self._repository.get_subscriptions(user_id=user_id)
        except NoResultFound as exc:
            raise UserNotFound(f"User with id {user_id} not found") from exc

        users = users[offset : offset + limit]
        return [
            UserGet(
                id=user.id,
                username=user.username,
                email=user.email,
                telegram_username=user.telegram_username,
                is_verified_email=user.is_verified_email,
                is_verified_telegram=user.is_verified_telegram,
                subscribers_count=user.subscribers_count,
                is_subscribed=(curr_user and (curr_user.id in [u.id for u in user.subscribers])),
            )
            for user in users
        ]
