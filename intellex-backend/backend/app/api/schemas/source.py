from datetime import datetime

from pydantic import BaseModel


class SourceStats(BaseModel):
    name: str

    document_count: int

    last_collected_at: datetime | None


class SourceListResponse(BaseModel):
    items: list[SourceStats]
