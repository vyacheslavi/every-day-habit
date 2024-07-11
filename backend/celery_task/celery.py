from celery import Celery

from backend.app.core.config import settings


celery_app = Celery(
    "tasks",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend_url,
    include=["backend.celery_task.tasks"],
)
