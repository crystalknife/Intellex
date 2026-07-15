"""
Collection Repository

Persistence access for user-created collections of saved documents and
events.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from backend.app.db.models import CollectionItemModel, CollectionModel


class DuplicateItemError(Exception):
    """Raised when the same document/event is already saved to this collection."""


class CollectionRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[CollectionModel]:
        stmt = (
            select(CollectionModel)
            .options(selectinload(CollectionModel.items))
            .order_by(CollectionModel.updated_at.desc())
        )

        return list(self.db.execute(stmt).scalars())

    def get(self, collection_id: str) -> CollectionModel | None:
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
            .where(CollectionModel.id == collection_id)
        )

        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, name: str) -> CollectionModel:
        model = CollectionModel(name=name)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def rename(self, collection_id: str, name: str) -> CollectionModel | None:
        model = self.db.get(CollectionModel, collection_id)

        if model is None:
            return None

        model.name = name
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete(self, collection_id: str) -> bool:
        model = self.db.get(CollectionModel, collection_id)

        if model is None:
            return False

        self.db.delete(model)
        self.db.commit()

        return True

    def add_document(
        self, collection_id: str, document_id: str
    ) -> CollectionItemModel:
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
        self, collection_id: str, event_id: str
    ) -> CollectionItemModel:
        item = CollectionItemModel(
            collection_id=collection_id, event_id=event_id
        )

        self.db.add(item)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise DuplicateItemError()

        self.db.refresh(item)

        return item

    def remove_item(self, collection_id: str, item_id: str) -> bool:
        item = self.db.get(CollectionItemModel, item_id)

        if item is None or item.collection_id != collection_id:
            return False

        self.db.delete(item)
        self.db.commit()

        return True
