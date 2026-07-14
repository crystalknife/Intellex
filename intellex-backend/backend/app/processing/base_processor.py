"""
Base Processor

Every processing stage in Intellex inherits from this class.
"""

from abc import ABC, abstractmethod

from backend.app.domain.document import Document


class Processor(ABC):
    """
    Base processor interface.
    """

    @abstractmethod
    async def process(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Process documents.
        """
        raise NotImplementedError