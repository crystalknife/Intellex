from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str

    title: str

    summary: str

    url: str

    source: str

    author: str | None

    language: str

    category: str

    entities: dict[str, list[str]]

    keywords: list[str]

    published_at: datetime | None

    collected_at: datetime

    event_id: str | None = None


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]

    total: int

    limit: int

    offset: int
