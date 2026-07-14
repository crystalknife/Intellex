"""
Event Repository

All persistence access for events goes through here.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from backend.app.db.models import DocumentModel, EventModel
from backend.app.domain.event import Event


class EventRepository:
    """Persistence access for Event records."""

    def __init__(self, db: Session):
        self.db = db

    def replace_all(self, events: list[Event]) -> list[EventModel]:
        """
        Replace the entire event clustering with a freshly computed one.

        Events are cheap to fully recompute from the current document set
        on every ingestion cycle (EventBuilder is deterministic given the
        same documents), so rather than trying to diff/merge clusters
        across runs, we clear the previous generation and re-derive event
        assignment on every document. Document rows themselves are never
        touched here -- only their `event_id` foreign key.
        """

        # Detach every document from its current event, then delete all
        # existing event rows.
        self.db.query(DocumentModel).update({DocumentModel.event_id: None})
        self.db.query(EventModel).delete()

        document_ids = {
            str(doc_id)
            for event in events
            for doc_id in event.document_ids
        }

        documents_by_id = {
            model.id: model
            for model in self.db.execute(
                select(DocumentModel).where(
                    DocumentModel.id.in_(document_ids)
                )
            ).scalars()
        } if document_ids else {}

        created: list[EventModel] = []

        for event in events:
            model = EventModel(
                id=str(event.id),
                title=event.title,
                summary=event.summary,
                entities=event.entities,
                keywords=event.keywords,
                created_at=event.created_at,
            )

            self.db.add(model)
            created.append(model)

            for doc_id in event.document_ids:
                document = documents_by_id.get(str(doc_id))

                if document:
                    document.event = model

        self.db.commit()

        return created

    def list_events(
        self, limit: int = 20, offset: int = 0
    ) -> tuple[list[EventModel], int]:
        total = self.db.execute(
            select(func.count()).select_from(EventModel)
        ).scalar_one()

        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.documents))
            .order_by(EventModel.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )

        results = self.db.execute(stmt).scalars().all()

        return list(results), total

    def get(self, event_id: str) -> EventModel | None:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.documents))
            .where(EventModel.id == event_id)
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def count(self) -> int:
        return self.db.execute(
            select(func.count()).select_from(EventModel)
        ).scalar_one()
