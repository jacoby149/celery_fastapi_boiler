from celery import Celery
import settings

celery_app = Celery(
        "celery_test",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_BROKER_URL
        )
