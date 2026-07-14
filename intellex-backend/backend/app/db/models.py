"""
Database Models

SQLAlchemy ORM models mirroring the Intellex domain models
(app/domain/document.py, app/domain/event.py). These are the tables that
back the repository layer -- documents and the events they get clustered
into are both persisted here so the API never has to re-run the
collection pipeline synchronously on request.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


def _uuid_str() -> str:
    return str(uuid4())


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    title: Mapped[str] = mapped_column(String(512))

    summary: Mapped[str] = mapped_column(Text, default="")

    entities: Mapped[dict] = mapped_column(JSON, default=dict)

    keywords: Mapped[list] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    documents: Mapped[list["DocumentModel"]] = relationship(
        "DocumentModel",
        back_populates="event",
        order_by="DocumentModel.published_at.desc()",
    )


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    title: Mapped[str] = mapped_column(String(1024))

    content: Mapped[str] = mapped_column(Text, default="")

    summary: Mapped[str] = mapped_column(Text, default="")

    # Natural key. Used to upsert documents across ingestion cycles so IDs
    # stay stable (and duplicates from re-fetching the same feed are never
    # inserted twice).
    url: Mapped[str] = mapped_column(
        String(2048), unique=True, index=True
    )

    source: Mapped[str] = mapped_column(String(256), index=True)

    author: Mapped[str | None] = mapped_column(String(256), nullable=True)

    language: Mapped[str] = mapped_column(String(16), default="en")

    category: Mapped[str] = mapped_column(
        String(64), default="general", index=True
    )

    tags: Mapped[list] = mapped_column(JSON, default=list)

    entities: Mapped[dict] = mapped_column(JSON, default=dict)

    keywords: Mapped[list] = mapped_column(JSON, default=list)

    doc_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    event_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("events.id"), nullable=True, index=True
    )

    event: Mapped["EventModel | None"] = relationship(
        "EventModel", back_populates="documents"
    )

    __table_args__ = (
        Index("ix_documents_published_at", "published_at"),
    )


class FeedSourceModel(Base):
    """
    A configured RSS feed. Replaces the previous hardcoded feed list --
    RSSCollector reads enabled feeds from this table fresh on every
    ingestion cycle, so adding/removing a feed here takes effect on the
    next scheduled run without a restart or code change.
    """

    __tablename__ = "feed_sources"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    url: Mapped[str] = mapped_column(String(2048), unique=True)

    label: Mapped[str] = mapped_column(String(256), default="")

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
