"""
RSS Collector

Downloads RSS feeds and converts them into Document objects.
"""

import asyncio

import feedparser

from backend.app.domain.document import Document
from backend.app.interfaces.collector import Collector
from backend.app.processing.rss_parser import RSSParser


DEFAULT_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "http://feeds.arstechnica.com/arstechnica/index",
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
]


class RSSCollector(Collector):
    """
    RSS Feed Collector.
    """

    def __init__(self, feeds: list[str] | None = None):
        # Explicit override (used by tests / callers that don't want
        # DB-driven feed configuration). When None, feeds are resolved
        # fresh from the database on every collect() call instead --
        # this is what lets feeds be added/removed/toggled via the API
        # and take effect on the next ingestion cycle without a restart.
        self._static_feeds = feeds

    async def collect(self) -> list[Document]:
        # feedparser.parse() performs a blocking HTTP request per feed.
        # Run it in a worker thread so sequential network round-trips
        # don't freeze the event loop that's also serving API requests.
        return await asyncio.to_thread(self._collect_sync)

    def _resolve_feeds(self) -> list[str]:
        if self._static_feeds is not None:
            return self._static_feeds

        # Local import to avoid a circular import at module load time
        # (db/repositories import from app.db which is fine, but keeping
        # this import local mirrors how the rest of the codebase avoids
        # importing the DB layer at collector-module import time).
        from backend.app.db.session import SessionLocal
        from backend.app.repositories.feed_source_repository import (
            FeedSourceRepository,
        )

        db = SessionLocal()

        try:
            repo = FeedSourceRepository(db)
            repo.seed_defaults_if_empty(DEFAULT_FEEDS)

            return [f.url for f in repo.list_all(enabled_only=True)]
        finally:
            db.close()

    def _collect_sync(self) -> list[Document]:

        documents: list[Document] = []

        for url in self._resolve_feeds():

            feed = feedparser.parse(
                url,
                agent=(
                    "Mozilla/5.0 (compatible; IntellexBot/1.0; "
                    "+https://intellex.local)"
                ),
            )

            source = feed.feed.get("title", "RSS")

            for entry in feed.entries:

                try:

                    document = RSSParser.parse(
                        entry,
                        source,
                    )

                    documents.append(document)

                except Exception as e:

                    print(f"[RSS Parser Error] {e}")

        return documents