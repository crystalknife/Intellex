"""
Entity Processor

Adds extracted entities to each Document.
"""

import asyncio

from backend.app.domain.document import Document
from backend.app.processing.base_processor import Processor
from backend.app.services.entity_service import EntityService


class EntityProcessor(Processor):

    async def process(
        self,
        documents: list[Document],
    ) -> list[Document]:
        # spaCy NER is CPU-bound and synchronous; running it directly
        # inside an async function still blocks the event loop for the
        # entire batch. Offload the whole batch to a worker thread so
        # the API server stays responsive to requests while this runs.
        return await asyncio.to_thread(self._process_sync, documents)

    @staticmethod
    def _process_sync(documents: list[Document]) -> list[Document]:

        for document in documents:

            text = " ".join(
                [
                    document.title,
                    document.summary,
                    document.content,
                ]
            )

            entities = EntityService.extract(text)

            document.entities = entities

        return documents
