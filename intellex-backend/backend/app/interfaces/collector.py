"""
Collector Interface

Every data source in Intellex must implement this interface.
"""

from abc import ABC, abstractmethod

from backend.app.domain.document import Document


class Collector(ABC):
    """
    Base interface for every Intellex collector.
    """

    @abstractmethod
    async def collect(self) -> list[Document]:
        """
        Collect documents from an external source.
        """
        raise NotImplementedError