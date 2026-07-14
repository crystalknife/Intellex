"""
Keyword Processor
"""

import asyncio

from backend.app.domain.document import Document
from backend.app.processing.base_processor import Processor
from backend.app.services.keyword_service import KeywordService


class KeywordProcessor(Processor):

    async def process(
        self,
        documents: list[Document],
    ) -> list[Document]:
        # Same reasoning as EntityProcessor: spaCy parsing is CPU-bound
        # and synchronous, so it needs to run off the event loop.
        return await asyncio.to_thread(self._process_sync, documents)

    @staticmethod
    def _process_sync(documents: list[Document]) -> list[Document]:

        for document in documents:

            text = " ".join([
                document.summary,
                document.content,
            ])

            document.keywords = KeywordService.extract(
                text, title=document.title
            )

        return documents
