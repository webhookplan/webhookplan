from .celery import celery_app
from tasks.debug_task import debug_task

__all__ = ("celery_app",)
