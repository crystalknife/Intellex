"""
Intellex Event Domain Model
"""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Event(BaseModel):
    """
    Represents a real-world event composed of one or more documents.
    """

    id: UUID = Field(default_factory=uuid4)

    title: str

    summary: str = ""

    document_ids: list[UUID] = Field(default_factory=list)

    entities: dict[str, list[str]] = Field(default_factory=dict)

    keywords: list[str] = Field(default_factory=list)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )