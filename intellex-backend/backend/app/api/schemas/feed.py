from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class FeedSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    url: str
    label: str
    enabled: bool
    created_at: datetime


class FeedSourceListResponse(BaseModel):
    items: list[FeedSourceResponse]


class FeedSourceCreateRequest(BaseModel):
    url: str
    label: str = ""

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        value = value.strip()

        if not value.startswith(("http://", "https://")):
            raise ValueError("Feed URL must start with http:// or https://")

        return value


class FeedSourceUpdateRequest(BaseModel):
    enabled: bool
