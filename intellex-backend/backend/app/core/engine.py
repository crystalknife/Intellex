"""
Intellex Engine
"""

from backend.app.collectors.rss import RSSCollector
from backend.app.core.logger import get_logger
from backend.app.domain.document import Document
from backend.app.pipeline.document_pipeline import DocumentPipeline
from backend.app.processing.duplicate_processor import DuplicateProcessor
from backend.app.processing.entity_processor import EntityProcessor
from backend.app.processing.keyword_processor import KeywordProcessor


logger = get_logger("Engine")


class IntellexEngine:

    def __init__(self):

        logger.info("Initializing Engine")

        self.collector = RSSCollector()

        from backend.app.processing.normalization_processor import (
            NormalizationProcessor,
        )

        self.pipeline = DocumentPipeline()

        self.pipeline.add_processor(
            NormalizationProcessor()
        )

        self.pipeline.add_processor(
            DuplicateProcessor()
        )
        
        self.pipeline.add_processor(
            EntityProcessor()
        )
       
        self.pipeline.add_processor(
            KeywordProcessor()
        )

    async def run(self) -> list[Document]:

        logger.info("Collecting documents")

        documents = await self.collector.collect()

        logger.info(f"Collected {len(documents)} documents")

        logger.info("Running pipeline")

        documents = await self.pipeline.run(documents)

        logger.info(
            f"Pipeline completed ({len(documents)} unique documents)"
        )

        return documents