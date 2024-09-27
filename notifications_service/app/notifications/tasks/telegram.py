import requests

from app.config import settings
from app.notifications.tasks.app import celery_app
from app.notifications.tasks.exceptions import CantSendNotification


def get_chat_id_by_username(username: str) -> int:  # type: ignore
    url = f"https://api.telegram.org/bot{settings.telegram.token}/getUpdates"

    res = requests.get(url)

    for update in res.json()["result"]:
        if update["message"]["from"]["username"] == username:
            return update["message"]["chat"]["id"]


def send_telegram_message(username: str, message: str) -> bool:
    chat_id = get_chat_id_by_username(username)
    url = f"https://api.telegram.org/bot{settings.telegram.token}/sendMessage?chat_id={chat_id}&text={message}"

    res = requests.post(url)
    return res.status_code == 200


@celery_app.task
def send_telegram_notification(username: str, message: str) -> None:
    if not send_telegram_message(username, message):
        raise CantSendNotification("Failed to send telegram message")
