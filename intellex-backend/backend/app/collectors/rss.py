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
        # Feeds are always passed in explicitly by the caller now.
        # FeedSourceRepository is organization-scoped (feed configuration
        # is private per org, see Phase B), so this collector has no
        # business resolving "the" feed list from the DB itself anymore
        # -- IngestionService resolves the calling organization's
        # enabled feeds and passes them in per cycle. `None` falls back
        # to DEFAULT_FEEDS, which only exists to keep the standalone
        # debug entrypoint (IntellexEngine's default construction,
        # main.py) usable without a DB/org context.
        self._static_feeds = feeds

    async def collect(self) -> list[Document]:
        # feedparser.parse() performs a blocking HTTP request per feed.
        # Run it in a worker thread so sequential network round-trips
        # don't freeze the event loop that's also serving API requests.
        return await asyncio.to_thread(self._collect_sync)

    def _resolve_feeds(self) -> list[str]:
        if self._static_feeds is not None:
            return self._static_feeds

        return DEFAULT_FEEDS

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