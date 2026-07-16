"""
Event Repository

All persistence access for events goes through here. Every method is
scoped to a single organization_id -- events are private per
organization, same as documents (see DocumentRepository).
"""

from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from backend.app.db.models import DocumentModel, EventModel
from backend.app.domain.event import Event


class EventRepository:
    """Persistence access for Event records, scoped per organization."""

    def __init__(self, db: Session):
        self.db = db

    def replace_all(
        self, events: list[Event], organization_id: str
    ) -> list[EventModel]:
        """
        Replace this organization's entire event clustering with a
        freshly computed one. Events are cheap to fully recompute from
        the org's current document set on every ingestion cycle
        (EventBuilder is deterministic given the same documents), so
        rather than trying to diff/merge clusters across runs, we clear
        this org's previous generation and re-derive event assignment.

        Scoped strictly to organization_id on both the reset and the
        delete -- this must never touch another organization's events
        or documents.
        """

        self.db.query(DocumentModel).filter(
            DocumentModel.organization_id == organization_id
        ).update({DocumentModel.event_id: None})

        self.db.query(EventModel).filter(
            EventModel.organization_id == organization_id
        ).delete()

        document_ids = {
            str(doc_id)
            for event in events
            for doc_id in event.document_ids
        }

        documents_by_id = {
            model.id: model
            for model in self.db.execute(
                select(DocumentModel).where(
                    DocumentModel.organization_id == organization_id,
                    DocumentModel.id.in_(document_ids),
                )
            ).scalars()
        } if document_ids else {}

        created: list[EventModel] = []

        for event in events:
            model = EventModel(
                id=str(event.id),
                organization_id=organization_id,
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
        self, organization_id: str, limit: int = 20, offset: int = 0
    ) -> tuple[list[EventModel], int]:
        total = self.db.execute(
            select(func.count())
            .select_from(EventModel)
            .where(EventModel.organization_id == organization_id)
        ).scalar_one()

        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.documents))
            .where(EventModel.organization_id == organization_id)
            .order_by(EventModel.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )

        results = self.db.execute(stmt).scalars().all()

        return list(results), total

    def get(
        self, event_id: str, organization_id: str
    ) -> EventModel | None:
        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.documents))
            .where(
                EventModel.id == event_id,
                EventModel.organization_id == organization_id,
            )
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def count(self, organization_id: str) -> int:
        return self.db.execute(
            select(func.count())
            .select_from(EventModel)
            .where(EventModel.organization_id == organization_id)
        ).scalar_one()

    def search(
        self, query: str, organization_id: str, limit: int = 20
    ) -> tuple[list[EventModel], int]:
        pattern = f"%{query}%"

        stmt = (
            select(EventModel)
            .options(selectinload(EventModel.documents))
            .where(
                EventModel.organization_id == organization_id,
                or_(
                    EventModel.title.ilike(pattern),
                    EventModel.summary.ilike(pattern),
                ),
            )
        )

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        stmt = stmt.order_by(EventModel.updated_at.desc()).limit(limit)

        results = self.db.execute(stmt).scalars().all()

        return list(results), total
