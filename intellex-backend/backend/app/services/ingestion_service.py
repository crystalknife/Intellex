"""
Ingestion Service

Orchestrates a full ingestion cycle: collect -> process -> persist ->
re-cluster into events. This is the single place that both the startup
hook and the background scheduler call into -- routers never trigger
collection themselves anymore, they only ever read from the database.
"""

from datetime import datetime, UTC

import asyncio

from sqlalchemy.orm import Session

from backend.app.core.engine import IntellexEngine
from backend.app.core.logger import get_logger
from backend.app.db.models import DocumentModel
from backend.app.db.session import SessionLocal
from backend.app.domain.document import Document
from backend.app.repositories.document_repository import DocumentRepository
from backend.app.repositories.event_repository import EventRepository
from backend.app.services.event_builder import EventBuilder

logger = get_logger("IngestionService")


def _model_to_domain(model: DocumentModel) -> Document:
    return Document(
        id=model.id,
        title=model.title,
        content=model.content,
        summary=model.summary,
        url=model.url,
        source=model.source,
        author=model.author,
        language=model.language,
        category=model.category,
        tags=model.tags or [],
        entities=model.entities or {},
        keywords=model.keywords or [],
        metadata=model.doc_metadata or {},
        published_at=model.published_at,
        collected_at=model.collected_at,
    )


class IngestionService:
    """Runs and persists a full collect -> process -> cluster cycle."""

    def __init__(self):
        self.engine = IntellexEngine()
        self.last_run_at: datetime | None = None
        self.last_run_fetched_count: int = 0
        self.last_run_unique_count: int = 0
        self.is_running: bool = False

    async def run_cycle(self, db: Session | None = None) -> dict:
        if self.is_running:
            logger.warning("Ingestion cycle already in progress, skipping")
            return {"skipped": True}

        self.is_running = True
        owns_session = db is None
        db = db or SessionLocal()

        try:
            logger.info("Starting ingestion cycle")

            raw_documents = await self.engine.collector.collect()
            fetched_count = len(raw_documents)

            processed_documents = await self.engine.pipeline.run(
                raw_documents
            )
            unique_count = len(processed_documents)

            document_repo = DocumentRepository(db)
            await asyncio.to_thread(
                document_repo.bulk_upsert, processed_documents
            )

            # Re-cluster across the *entire* corpus (not just this cycle's
            # batch) so events keep accumulating new documents over time
            # instead of resetting every run.
            all_documents, _ = await asyncio.to_thread(
                document_repo.list_documents, limit=10_000, offset=0
            )
            domain_documents = [
                _model_to_domain(model) for model in all_documents
            ]

            events = await asyncio.to_thread(
                EventBuilder.build, domain_documents
            )

            event_repo = EventRepository(db)
            await asyncio.to_thread(event_repo.replace_all, events)

            self.last_run_at = datetime.now(UTC)
            self.last_run_fetched_count = fetched_count
            self.last_run_unique_count = unique_count

            logger.info(
                f"Ingestion cycle complete: {fetched_count} fetched, "
                f"{unique_count} unique this cycle, "
                f"{document_repo.count()} total documents, "
                f"{event_repo.count()} events"
            )

            return {
                "fetched": fetched_count,
                "unique": unique_count,
                "total_documents": document_repo.count(),
                "total_events": event_repo.count(),
            }

        except Exception:
            logger.exception("Ingestion cycle failed")
            db.rollback()
            raise
        finally:
            self.is_running = False
            if owns_session:
                db.close()


ingestion_service = IngestionService()
