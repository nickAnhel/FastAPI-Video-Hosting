from celery import Celery


celery_app = Celery("tasks", broker="redis://redis:6379")
celery_app.autodiscover_tasks(
    [
        "app.notifications.tasks.console",
        "app.notifications.tasks.email",
        "app.notifications.tasks.telegram",
    ],
    force=True,
)
