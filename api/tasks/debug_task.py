from core.celery import celery_app


@celery_app.task(bind=True)
def debug_task(*args, **kwargs):
    print(f"[DEBUG_TASK]: Hello, World!")
