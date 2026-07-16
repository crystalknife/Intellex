"""
Collection Repository

Persistence access for user-created collections of saved documents and
events. Every method is scoped to a single organization_id -- a
collection belongs to one org, and the documents/events saved into it
must belong to that same org (checked explicitly in add_document /
add_event as defense-in-depth, even though callers should already only
ever pass IDs they fetched within their own org's scope).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from backend.app.db.models import (
    CollectionItemModel,
    CollectionModel,
    DocumentModel,
    EventModel,
)


class DuplicateItemError(Exception):
    """Raised when the same document/event is already saved to this collection."""


class CrossOrganizationReferenceError(Exception):
    """Raised when a document/event doesn't belong to the collection's org."""


class CollectionRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(self, organization_id: str) -> list[CollectionModel]:
        stmt = (
            select(CollectionModel)
            .options(selectinload(CollectionModel.items))
            .where(CollectionModel.organization_id == organization_id)
            .order_by(CollectionModel.updated_at.desc())
        )

        return list(self.db.execute(stmt).scalars())

    def get(
        self, collection_id: str, organization_id: str
    ) -> CollectionModel | None:
        stmt = (
            select(CollectionModel)
            .options(
                selectinload(CollectionModel.items).selectinload(
                    CollectionItemModel.document
                ),
                selectinload(CollectionModel.items).selectinload(
                    CollectionItemModel.event
                ),
            )
            .where(
                CollectionModel.id == collection_id,
                CollectionModel.organization_id == organization_id,
            )
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, name: str, organization_id: str) -> CollectionModel:
        model = CollectionModel(name=name, organization_id=organization_id)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def rename(
        self, collection_id: str, organization_id: str, name: str
    ) -> CollectionModel | None:
        model = self.get(collection_id, organization_id)

        if model is None:
            return None

        model.name = name
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete(self, collection_id: str, organization_id: str) -> bool:
        model = self.get(collection_id, organization_id)

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True

    def add_document(
        self, collection_id: str, document_id: str, organization_id: str
    ) -> CollectionItemModel:
        document = self.db.execute(
            select(DocumentModel.id).where(
                DocumentModel.id == document_id,
                DocumentModel.organization_id == organization_id,
            )
        ).scalar_one_or_none()

        if document is None:
            raise CrossOrganizationReferenceError()

        item = CollectionItemModel(
            collection_id=collection_id, document_id=document_id
        )

        self.db.add(item)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateItemError()

        self.db.refresh(item)

        return item

    def add_event(
        self, collection_id: str, event_id: str, organization_id: str
    ) -> CollectionItemModel:
        event = self.db.execute(
            select(EventModel.id).where(
                EventModel.id == event_id,
                EventModel.organization_id == organization_id,
            )
        ).scalar_one_or_none()

        if event is None:
            raise CrossOrganizationReferenceError()

        item = CollectionItemModel(collection_id=collection_id, event_id=event_id)

        self.db.add(item)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateItemError()

        self.db.refresh(item)

        return item

    def remove_item(
        self, collection_id: str, item_id: str, organization_id: str
    ) -> bool:
        # Confirms the collection itself belongs to this org before
        # touching the item -- same belt-and-suspenders reasoning as
        # add_document/add_event above.
        collection = self.get(collection_id, organization_id)

        if collection is None:
            return False

        item = self.db.get(CollectionItemModel, item_id)

        if item is None or item.collection_id != collection_id:
            return False

        self.db.delete(item)
        self.db.commit()

        return True
