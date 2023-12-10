from core.celery import celery_app
from config import (
    JITTER_MAX_RETRIES,
    JITTER_RETRY_BACKOFF,
    JITTER_RETRY_BACKOFF_MAX,
    JITTER_RETRY_JITTER,
)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    max_retries=JITTER_MAX_RETRIES,
    retry_backoff=JITTER_RETRY_BACKOFF,
    retry_backoff_max=JITTER_RETRY_BACKOFF_MAX,
    retry_jitter=JITTER_RETRY_JITTER,
)
def debug_task(self, *args, **kwargs):
    print(f"[START]: DEBUG_TASK")
    print(f"{self=}")
    print(f"{args=}")
    print(f"{kwargs=}")
    print(f"[END]: DEBUG_TASK")

    raise Exception
