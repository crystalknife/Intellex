from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.schemas import PipelineStatsResponse
from backend.app.config import settings
from backend.app.db.session import get_db
from backend.app.repositories.document_repository import DocumentRepository
from backend.app.repositories.event_repository import EventRepository
from backend.app.services.ingestion_service import ingestion_service

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/pipeline", response_model=PipelineStatsResponse)
async def get_pipeline_stats(db: Session = Depends(get_db)):
    document_repo = DocumentRepository(db)
    event_repo = EventRepository(db)

    total_documents = document_repo.count()
    total_events = event_repo.count()
    sources = document_repo.distinct_sources()

    fetched = ingestion_service.last_run_fetched_count
    unique = ingestion_service.last_run_unique_count

    dedup_rate = (
        round(((fetched - unique) / fetched) * 100, 1)
        if fetched
        else 0.0
    )

    return PipelineStatsResponse(
        total_documents=total_documents,
        total_events=total_events,
        total_sources=len(sources),
        sources=sources,
        last_run_at=ingestion_service.last_run_at,
        last_run_fetched=fetched,
        last_run_unique=unique,
        dedup_rate=dedup_rate,
        refresh_interval_minutes=settings.REFRESH_INTERVAL_MINUTES,
        is_running=ingestion_service.is_running,
    )
