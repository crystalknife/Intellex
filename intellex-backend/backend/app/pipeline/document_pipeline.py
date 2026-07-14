"""
Intellex Processing Pipeline
"""

from backend.app.domain.document import Document
from backend.app.processing.base_processor import Processor


class DocumentPipeline:
    """
    Executes processors sequentially.
    """

    def __init__(self):

        self.processors: list[Processor] = []

    def add_processor(
        self,
        processor: Processor,
    ):

        self.processors.append(processor)

    async def run(
        self,
        documents: list[Document],
    ) -> list[Document]:

        current = documents

        for processor in self.processors:

            current = await processor.process(current)

        return current