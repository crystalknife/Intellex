"""
Ingestion Scheduler

A minimal asyncio-based recurring job runner. Deliberately avoids pulling
in APScheduler/Celery for a single periodic job -- this is the smallest
correct implementation, and it can be swapped for a heavier scheduler
later without changing IngestionService's interface.

Phase B: ingestion is private per organization, so each tick runs one
cycle per existing organization (sequentially, not concurrently -- see
_run_all_orgs for why). A brand-new install with zero signed-up
organizations simply runs zero cycles until the first signup exists.
"""

import asyncio

from backend.app.config import settings
from backend.app.core.logger import get_logger
from backend.app.db.session import SessionLocal
from backend.app.repositories.organization_repository import (
    OrganizationRepository,
)
from backend.app.services.ingestion_service import ingestion_service

logger = get_logger("Scheduler")

_task: asyncio.Task | None = None


async def _run_all_orgs() -> None:
    db = SessionLocal()

    try:
        organizations = OrganizationRepository(db).list_all()
    finally:
        db.close()

    if not organizations:
        logger.info("No organizations exist yet -- skipping ingestion tick")
        return

    # Sequential, not asyncio.gather'd concurrently -- every org's cycle
    # shares one IntellexEngine/pipeline instance (see IngestionService),
    # and running org cycles one at a time keeps that shared, stateful
    # pipeline usage simple and predictable rather than needing it to be
    # concurrency-safe across simultaneous callers.
    for org in organizations:
        try:
            await ingestion_service.run_cycle(organization_id=org.id)
        except Exception:
            # Already logged inside run_cycle; one organization's feed
            # outage or processing error must never stop the scheduler
            # from continuing on to the next organization, let alone
            # taking down the whole loop.
            pass


async def _loop() -> None:
    interval_seconds = settings.REFRESH_INTERVAL_MINUTES * 60

    if settings.RUN_INGESTION_ON_STARTUP:
        await _run_all_orgs()

    while True:
        await asyncio.sleep(interval_seconds)
        await _run_all_orgs()


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
