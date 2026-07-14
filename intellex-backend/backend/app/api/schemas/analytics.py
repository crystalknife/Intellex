from datetime import datetime

from pydantic import BaseModel


class PipelineStatsResponse(BaseModel):
    total_documents: int

    total_events: int

    total_sources: int

    sources: list[str]

    last_run_at: datetime | None

    last_run_fetched: int

    last_run_unique: int

    dedup_rate: float

    refresh_interval_minutes: int

    is_running: bool
