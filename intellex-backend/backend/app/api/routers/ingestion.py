import asyncio

from fastapi import APIRouter

from backend.app.services.ingestion_service import ingestion_service

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)


@router.post("/trigger", status_code=202)
async def trigger_ingestion():
    """
    Kick off an ingestion cycle immediately instead of waiting for the
    next scheduled interval -- primarily so a newly added feed can be
    verified right away. Fires and returns immediately; poll
    /analytics/pipeline (isRunning / lastRunAt) for progress.
    """

    if ingestion_service.is_running:
        return {"status": "already_running"}

    asyncio.create_task(ingestion_service.run_cycle())

    return {"status": "started"}
