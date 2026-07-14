"""
Normalization Processor

Normalizes documents before further processing.
"""

import html
import re

from backend.app.domain.document import Document
from backend.app.processing.base_processor import Processor


class NormalizationProcessor(Processor):

    async def process(
        self,
        documents: list[Document],
    ) -> list[Document]:

        for doc in documents:

            doc.title = self._normalize_text(doc.title)

            doc.summary = self._normalize_text(doc.summary)

            doc.content = self._normalize_text(doc.content)

        return documents

    @staticmethod
    def _normalize_text(text: str) -> str:

        # Some feeds double-encode or leave raw numeric entities
        # (e.g. "&#8217;") in titles/summaries even after feedparser's
        # own decoding -- unescape defensively so these never reach the
        # UI as literal "&#8217;" text.
        text = html.unescape(text)

        text = text.strip()

        text = re.sub(r"\s+", " ", text)

        text = text.replace("\n", " ")

        return text