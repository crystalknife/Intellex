from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from backend.app.api.schemas.document import DocumentResponse
from backend.app.api.schemas.event import EventResponse


class CollectionResponse(BaseModel):
    id: str
    name: str
    item_count: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model) -> "CollectionResponse":
        return cls(
            id=model.id,
            name=model.name,
            item_count=len(model.items),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class CollectionListResponse(BaseModel):
    items: list[CollectionResponse]

    @classmethod
    def build(cls, models) -> "CollectionListResponse":
        return cls(items=[CollectionResponse.from_model(m) for m in models])


class CollectionItemResponse(BaseModel):
    id: str
    type: Literal["document", "event"]
    added_at: datetime
    document: DocumentResponse | None = None
    event: EventResponse | None = None

    @classmethod
    def from_model(cls, model) -> "CollectionItemResponse":
        if model.document_id is not None:
            return cls(
                id=model.id,
                type="document",
                added_at=model.added_at,
                document=DocumentResponse.model_validate(model.document),
            )

        return cls(
            id=model.id,
            type="event",
            added_at=model.added_at,
            event=EventResponse.from_model(model.event),
        )


class CollectionDetailResponse(CollectionResponse):
    items: list[CollectionItemResponse] = []

    @classmethod
    def from_model(cls, model) -> "CollectionDetailResponse":
        return cls(
            id=model.id,
            name=model.name,
            item_count=len(model.items),
            created_at=model.created_at,
            updated_at=model.updated_at,
            items=[
                CollectionItemResponse.from_model(item)
                for item in model.items
            ],
        )


class CreateCollectionRequest(BaseModel):
    name: str


class RenameCollectionRequest(BaseModel):
    name: str


class AddCollectionItemRequest(BaseModel):
    type: Literal["document", "event"]
    id: str
