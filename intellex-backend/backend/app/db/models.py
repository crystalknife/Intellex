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

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


def _uuid_str() -> str:
    return str(uuid4())


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), index=True
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

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), index=True
    )

    title: Mapped[str] = mapped_column(String(1024))

    content: Mapped[str] = mapped_column(Text, default="")

    summary: Mapped[str] = mapped_column(Text, default="")

    # Natural key is (organization_id, url), not url alone -- two
    # organizations independently subscribed to the same RSS feed must
    # each get their own copy of the same article, since ingestion and
    # document storage are private per org. Upsert matching in
    # DocumentRepository filters on both columns together.
    url: Mapped[str] = mapped_column(String(2048), index=True)

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
        UniqueConstraint(
            "organization_id", "url", name="ux_document_org_url"
        ),
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

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), index=True
    )

    # Unique per (organization_id, url), not globally -- two orgs can
    # independently configure the same feed.
    url: Mapped[str] = mapped_column(String(2048))

    label: Mapped[str] = mapped_column(String(256), default="")

    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "url", name="ux_feed_org_url"),
    )


class CollectionModel(Base):
    """
    A user-created named group of saved documents and/or events.
    """

    __tablename__ = "collections"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), index=True
    )

    name: Mapped[str] = mapped_column(String(256))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    items: Mapped[list["CollectionItemModel"]] = relationship(
        "CollectionItemModel",
        back_populates="collection",
        cascade="all, delete-orphan",
        order_by="CollectionItemModel.added_at.desc()",
    )


class CollectionItemModel(Base):
    """
    A single saved document or event within a collection. Exactly one of
    document_id / event_id is set per row -- modeled as two nullable FKs
    rather than a separate join table per type so the collection detail
    view can query one table and get a naturally time-ordered mixed feed
    of saved items, regardless of type.
    """

    __tablename__ = "collection_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    collection_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("collections.id"), index=True
    )

    document_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("documents.id"), nullable=True
    )

    event_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("events.id"), nullable=True
    )

    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    collection: Mapped["CollectionModel"] = relationship(
        "CollectionModel", back_populates="items"
    )

    document: Mapped["DocumentModel | None"] = relationship("DocumentModel")

    event: Mapped["EventModel | None"] = relationship("EventModel")

    __table_args__ = (
        Index(
            "ux_collection_item_document",
            "collection_id",
            "document_id",
            unique=True,
        ),
        Index(
            "ux_collection_item_event",
            "collection_id",
            "event_id",
            unique=True,
        ),
    )


class UserModel(Base):
    """
    A person who can sign in. A user's organization membership (and
    therefore which org's data they see) lives in OrganizationMemberModel,
    not here -- kept separate so a user could belong to more than one
    organization later without changing this table.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)

    hashed_password: Mapped[str] = mapped_column(String(255))

    full_name: Mapped[str] = mapped_column(String(256), default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    memberships: Mapped[list["OrganizationMemberModel"]] = relationship(
        "OrganizationMemberModel", back_populates="user"
    )


class OrganizationModel(Base):
    """
    A tenant. Every piece of Intellex data will eventually be scoped to
    one of these (see Phase B of the auth rollout) -- documents, events,
    feeds, and collections are not yet org-scoped as of this migration,
    that retrofit is deliberately a separate, focused change.
    """

    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    name: Mapped[str] = mapped_column(String(256))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    members: Mapped[list["OrganizationMemberModel"]] = relationship(
        "OrganizationMemberModel", back_populates="organization"
    )


class OrganizationMemberModel(Base):
    """
    Join row linking a user to an organization with a role. A user has
    at most one membership per organization (enforced below); nothing
    today prevents multiple memberships across *different* orgs, which
    is intentional groundwork for future org-switching, even though the
    signup flow in Phase A only ever creates one.
    """

    __tablename__ = "organization_members"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=_uuid_str
    )

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), index=True
    )

    # "owner" | "admin" | "member" -- plain string rather than a DB enum
    # to match the rest of this file's style (category/language columns
    # are also plain strings) and to keep adding new roles a code-only
    # change.
    role: Mapped[str] = mapped_column(String(32), default="member")

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="memberships"
    )

    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", back_populates="members"
    )

    __table_args__ = (
        UniqueConstraint(
            "organization_id", "user_id", name="ux_org_member_unique"
        ),
    )
