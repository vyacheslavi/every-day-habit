from celery import Celery

from backend.app.core.config import settings


celery_app = Celery(
    "taska",
    broker=settings.celery.broker_url,
    include=["backend.celery_task.tasks"],
)
