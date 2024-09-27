from celery import shared_task

# from app.notifications.tasks.app import celery_app


@shared_task
def send_console_notification(message: str) -> None:
    print(message)
