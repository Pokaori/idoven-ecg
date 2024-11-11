from datetime import timedelta

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "ecg_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True,
    result_expires=timedelta(days=5),
    result_extended=True,
    include=["app.celery.worker"],
)
