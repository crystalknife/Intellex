from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.app.api.schemas.document import DocumentResponse


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str

    title: str

    summary: str

    keywords: list[str]

    entities: dict[str, list[str]]

    document_count: int = 0

    created_at: datetime

    updated_at: datetime

    @classmethod
    def from_model(cls, model) -> "EventResponse":
        return cls(
            id=model.id,
            title=model.title,
            summary=model.summary,
            keywords=model.keywords,
            entities=model.entities,
            document_count=len(model.documents),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class EventListResponse(BaseModel):
    items: list[EventResponse]

    total: int

    limit: int

    offset: int

    @classmethod
    def build(cls, models, total, limit, offset) -> "EventListResponse":
        return cls(
            items=[EventResponse.from_model(m) for m in models],
            total=total,
            limit=limit,
            offset=offset,
        )


class EventDetailResponse(EventResponse):
    documents: list[DocumentResponse] = []

    @classmethod
    def from_model(cls, model) -> "EventDetailResponse":
        return cls(
            id=model.id,
            title=model.title,
            summary=model.summary,
            keywords=model.keywords,
            entities=model.entities,
            document_count=len(model.documents),
            created_at=model.created_at,
            updated_at=model.updated_at,
            documents=[
                DocumentResponse.model_validate(d) for d in model.documents
            ],
        )
