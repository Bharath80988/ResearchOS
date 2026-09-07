from celery import Celery
from ..config import get_settings

settings = get_settings()

celery_app = Celery(
    "researchos_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_always_eager=settings.CELERY_TASK_ALWAYS_EAGER,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="execute_deep_research")
def execute_deep_research(research_id: str):
    """Background research job orchestrator (executed by Celery worker)."""
    # Celery task handler
    return {"research_id": research_id, "status": "completed"}
