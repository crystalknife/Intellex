"""
RSS Parser

Converts RSS feed entries into Intellex Document objects.
"""

from datetime import datetime, UTC
from typing import Any

from backend.app.domain.document import Document


class RSSParser:
    """Parses RSS feed entries into Document objects."""

    @staticmethod
    def parse(entry: Any, source: str) -> Document:
        """
        Convert a feedparser entry into a Document.

        Args:
            entry: FeedParser entry object.
            source: Source name.

        Returns:
            Document
        """

        return Document(
            title=entry.get("title", "").strip(),
            content=entry.get("summary", ""),
            summary=entry.get("summary", ""),
            url=entry.get("link", ""),
            source=source,
            author=entry.get("author"),
            published_at=RSSParser._parse_date(
                entry.get("published")
            ),
            metadata={
                "guid": entry.get("id"),
            },
        )

    @staticmethod
    def _parse_date(date_string: str | None):
        if not date_string:
            return None

        try:
            from email.utils import parsedate_to_datetime

            dt = parsedate_to_datetime(date_string)

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)

            return dt

        except Exception:
            return None