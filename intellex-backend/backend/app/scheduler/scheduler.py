"""
Ingestion Scheduler

A minimal asyncio-based recurring job runner. Deliberately avoids pulling
in APScheduler/Celery for a single periodic job -- this is the smallest
correct implementation, and it can be swapped for a heavier scheduler
later without changing IngestionService's interface.
"""

import asyncio

from backend.app.config import settings
from backend.app.core.logger import get_logger
from backend.app.services.ingestion_service import ingestion_service

logger = get_logger("Scheduler")

_task: asyncio.Task | None = None


async def _loop() -> None:
    interval_seconds = settings.REFRESH_INTERVAL_MINUTES * 60

    if settings.RUN_INGESTION_ON_STARTUP:
        try:
            await ingestion_service.run_cycle()
        except Exception:
            # Already logged inside run_cycle; the scheduler must keep
            # running even if a single cycle fails (e.g. transient feed
            # outage) so the app recovers on the next interval.
            pass

    while True:
        await asyncio.sleep(interval_seconds)

        try:
            await ingestion_service.run_cycle()
        except Exception:
            pass


def start() -> None:
    global _task

    if _task is not None:
        return

    logger.info(
        f"Starting ingestion scheduler "
        f"(every {settings.REFRESH_INTERVAL_MINUTES}m)"
    )

    _task = asyncio.create_task(_loop())


def stop() -> None:
    global _task

    if _task is not None:
        _task.cancel()
        _task = None
