"""
Ingestion Service

Orchestrates a full ingestion cycle: collect -> process -> persist ->
re-cluster into events. This is the single place that both the startup
hook and the background scheduler call into -- routers never trigger
collection themselves anymore, they only ever read from the database.

Phase B: ingestion is private per organization. There is no more
"the" ingestion cycle -- there is one cycle per organization, each
scoped to that org's own configured feeds and own document/event
corpus. A single shared IntellexEngine (and therefore a single shared,
expensive-to-load NLP pipeline) is reused across every org's cycle;
only the RSSCollector -- a cheap, stateless object -- is rebuilt per
cycle with that org's specific feed list.
"""

from datetime import datetime, UTC

import asyncio

from sqlalchemy.orm import Session

from backend.app.collectors.rss import DEFAULT_FEEDS, RSSCollector
from backend.app.core.engine import IntellexEngine
from backend.app.core.logger import get_logger
from backend.app.core.broadcaster import broadcaster
from backend.app.db.models import DocumentModel
from backend.app.db.session import SessionLocal
from backend.app.domain.document import Document
from backend.app.repositories.document_repository import DocumentRepository
from backend.app.repositories.event_repository import EventRepository
from backend.app.repositories.feed_source_repository import (
    FeedSourceRepository,
)
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


class OrgIngestionState:
    """Per-organization run bookkeeping (last run time, counts, etc.)."""

    def __init__(self) -> None:
        self.last_run_at: datetime | None = None
        self.last_run_fetched_count: int = 0
        self.last_run_unique_count: int = 0


class IngestionService:
    """Runs and persists a full collect -> process -> cluster cycle, per org."""

    def __init__(self):
        # Shared across every org's cycle -- holds the (expensive to
        # load) NLP pipeline. Its collector is never used directly;
        # each run_cycle() call builds its own org-scoped RSSCollector.
        self.engine = IntellexEngine()

        self._running_orgs: set[str] = set()
        self._state: dict[str, OrgIngestionState] = {}

    def is_running(self, organization_id: str) -> bool:
        return organization_id in self._running_orgs

    def get_state(self, organization_id: str) -> OrgIngestionState:
        return self._state.setdefault(organization_id, OrgIngestionState())

    async def run_cycle(
        self, organization_id: str, db: Session | None = None
    ) -> dict:
        if self.is_running(organization_id):
            logger.warning(
                f"Ingestion cycle already in progress for org "
                f"{organization_id}, skipping"
            )
            return {"skipped": True}

        self._running_orgs.add(organization_id)
        owns_session = db is None
        db = db or SessionLocal()

        await broadcaster.publish(organization_id, "ingestion_started", {})

        try:
            logger.info(f"Starting ingestion cycle for org {organization_id}")

            feed_repo = FeedSourceRepository(db)
            feed_repo.seed_defaults_if_empty(organization_id, DEFAULT_FEEDS)
            feed_urls = [
                f.url
                for f in feed_repo.list_all(organization_id, enabled_only=True)
            ]

            collector = RSSCollector(feeds=feed_urls)
            raw_documents = await collector.collect()
            fetched_count = len(raw_documents)

            processed_documents = await self.engine.pipeline.run(
                raw_documents
            )
            unique_count = len(processed_documents)

            document_repo = DocumentRepository(db)
            await asyncio.to_thread(
                document_repo.bulk_upsert, processed_documents, organization_id
            )

            # Re-cluster across this org's *entire* corpus (not just this
            # cycle's batch) so events keep accumulating new documents
            # over time instead of resetting every run.
            all_documents, _ = await asyncio.to_thread(
                document_repo.list_documents,
                organization_id,
                limit=10_000,
                offset=0,
            )
            domain_documents = [
                _model_to_domain(model) for model in all_documents
            ]

            events = await asyncio.to_thread(
                EventBuilder.build, domain_documents
            )

            event_repo = EventRepository(db)
            await asyncio.to_thread(
                event_repo.replace_all, events, organization_id
            )

            state = self.get_state(organization_id)
            state.last_run_at = datetime.now(UTC)
            state.last_run_fetched_count = fetched_count
            state.last_run_unique_count = unique_count

            total_documents = document_repo.count(organization_id)
            total_events = event_repo.count(organization_id)

            logger.info(
                f"Ingestion cycle complete for org {organization_id}: "
                f"{fetched_count} fetched, {unique_count} unique this "
                f"cycle, {total_documents} total documents, "
                f"{total_events} events"
            )

            result = {
                "fetched": fetched_count,
                "unique": unique_count,
                "total_documents": total_documents,
                "total_events": total_events,
            }

            await broadcaster.publish(
                organization_id, "ingestion_complete", result
            )

            return result

        except Exception:
            logger.exception(
                f"Ingestion cycle failed for org {organization_id}"
            )
            db.rollback()
            await broadcaster.publish(organization_id, "ingestion_failed", {})
            raise
        finally:
            self._running_orgs.discard(organization_id)
            if owns_session:
                db.close()


ingestion_service = IngestionService()
