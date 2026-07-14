"""
Intellex Domain Model
"""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class Document(BaseModel):
    """
    Canonical document model used throughout Intellex.
    """

    id: UUID = Field(default_factory=uuid4)

    title: str

    content: str = ""

    summary: str = ""

    url: HttpUrl

    source: str

    author: str | None = None

    language: str = "en"

    category: str = "general"

    tags: list[str] = Field(default_factory=list)

    # NEW
    entities: dict[str, list[str]] = Field(default_factory=dict)

    # NEW
    keywords: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    published_at: datetime | None = None

    collected_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )