"""
Duplicate Processor

Removes duplicate or highly similar documents.
"""

import asyncio

from rapidfuzz import fuzz

from backend.app.domain.document import Document
from backend.app.processing.base_processor import Processor


class DuplicateProcessor(Processor):

    def __init__(self, threshold: int = 90):

        self.threshold = threshold

    async def process(
        self,
        documents: list[Document],
    ) -> list[Document]:
        # O(n^2) fuzzy comparisons -- cheap per-pair, but the total can
        # grow non-trivially as the batch size grows. Keep it off the
        # event loop along with the rest of the pipeline.
        return await asyncio.to_thread(self._process_sync, documents)

    def _process_sync(self, documents: list[Document]) -> list[Document]:

        unique: list[Document] = []

        for document in documents:

            duplicate = False

            for existing in unique:

                similarity = fuzz.token_sort_ratio(
                    document.title,
                    existing.title,
                )

                if similarity >= self.threshold:
                    duplicate = True
                    break

            if not duplicate:
                unique.append(document)

        return unique