"""
Document Repository

All persistence access for documents goes through here. Routers and
processors never touch SQLAlchemy models or sessions directly.
"""

from __future__ import annotations

from datetime import datetime, UTC

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.app.db.models import DocumentModel
from backend.app.domain.document import Document


class DocumentRepository:
    """Persistence access for Document records."""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, document: Document) -> DocumentModel:
        """
        Insert a new document, or update an existing one matched by URL.

        URL is the natural key: the same article re-collected on a later
        ingestion cycle must resolve to the same row (and therefore the
        same stable ID) instead of creating a duplicate.
        """

        url = str(document.url)

        existing = self.db.execute(
            select(DocumentModel).where(DocumentModel.url == url)
        ).scalar_one_or_none()

        if existing:
            existing.title = document.title
            existing.content = document.content
            existing.summary = document.summary
            existing.source = document.source
            existing.author = document.author
            existing.language = document.language
            existing.category = document.category
            existing.tags = document.tags
            existing.entities = document.entities
            existing.keywords = document.keywords
            existing.doc_metadata = document.metadata
            existing.published_at = document.published_at
            return existing

        model = DocumentModel(
            id=str(document.id),
            title=document.title,
            content=document.content,
            summary=document.summary,
            url=url,
            source=document.source,
            author=document.author,
            language=document.language,
            category=document.category,
            tags=document.tags,
            entities=document.entities,
            keywords=document.keywords,
            doc_metadata=document.metadata,
            published_at=document.published_at,
            collected_at=document.collected_at,
        )

        self.db.add(model)

        return model

    def bulk_upsert(self, documents: list[Document]) -> list[DocumentModel]:
        models = [self.upsert(document) for document in documents]

        self.db.commit()

        return models

    def list_documents(
        self,
        limit: int = 20,
        offset: int = 0,
        source: str | None = None,
        category: str | None = None,
    ) -> tuple[list[DocumentModel], int]:
        query = select(DocumentModel)

        if source:
            query = query.where(DocumentModel.source == source)

        if category:
            query = query.where(DocumentModel.category == category)

        total = self.db.execute(
            select(func.count()).select_from(query.subquery())
        ).scalar_one()

        query = (
            query.order_by(DocumentModel.published_at.desc().nulls_last())
            .offset(offset)
            .limit(limit)
        )

        results = self.db.execute(query).scalars().all()

        return list(results), total

    def get(self, document_id: str) -> DocumentModel | None:
        return self.db.get(DocumentModel, document_id)

    def search(
        self, query: str, limit: int = 20
    ) -> tuple[list[DocumentModel], int]:
        pattern = f"%{query}%"

        stmt = select(DocumentModel).where(
            or_(
                DocumentModel.title.ilike(pattern),
                DocumentModel.summary.ilike(pattern),
                DocumentModel.content.ilike(pattern),
            )
        )

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        stmt = stmt.order_by(
            DocumentModel.published_at.desc().nulls_last()
        ).limit(limit)

        results = self.db.execute(stmt).scalars().all()

        return list(results), total

    def count(self) -> int:
        return self.db.execute(
            select(func.count()).select_from(DocumentModel)
        ).scalar_one()

    def distinct_sources(self) -> list[str]:
        rows = self.db.execute(
            select(DocumentModel.source).distinct()
        ).scalars().all()

        return list(rows)

    def counts_by_source(self) -> list[tuple[str, int]]:
        rows = self.db.execute(
            select(DocumentModel.source, func.count())
            .group_by(DocumentModel.source)
            .order_by(func.count().desc())
        ).all()

        return [(source, count) for source, count in rows]

    def most_recent_by_source(self) -> dict[str, datetime]:
        rows = self.db.execute(
            select(DocumentModel.source, func.max(DocumentModel.collected_at))
            .group_by(DocumentModel.source)
        ).all()

        return {source: collected_at for source, collected_at in rows}

    def most_recent_collected_at(self) -> datetime | None:
        return self.db.execute(
            select(func.max(DocumentModel.collected_at))
        ).scalar_one_or_none()
