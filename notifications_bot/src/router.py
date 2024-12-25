from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hlink

from sqlalchemy.exc import NoResultFound

import repository
from config import settings
from utils import create_url_safe_token


router = Router()


async def try_verify_telegram(message: Message) -> None:
    try:
        user = await repository.get_user(message.from_user.username)

        if not user.is_verified_telegram:
            verify_token = create_url_safe_token(
                data={"telegram_username": user.telegram_username, "chat_id": message.chat.id}
            )
            verify_link = hlink("link", f"{settings.backend_host}/users/telegram/verify/{verify_token}")

            await message.answer(
                f"To receive telegram notifications, please verify your telegram account by clicking on the {verify_link}",
                parse_mode="html",
            )
        else:
            await message.answer("Your Telegram account is verified")

    except NoResultFound:
        platfrom_link = hlink("ТипоTube", settings.frontend_host)
        profile_link = hlink("profile", f"{settings.frontend_host}/me/profile")

        await message.answer(
            f"Please register on {platfrom_link} and enter your telegram account in your {profile_link} to use this bot",
            parse_mode="html",
        )


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        "Welcome to ТипоTube Notifications bot!\n\nCommands:\n/start  - Start using bot and verify Telegram account\n/verify - Verify your Telegram account"
    )
    await try_verify_telegram(message)


@router.message(Command("verify"))
async def verify_command(message: Message) -> None:
    await try_verify_telegram(message)
