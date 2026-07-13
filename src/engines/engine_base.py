from abc import ABC, abstractmethod
from typing import List

from src.models.lead import Lead


class EngineBase(ABC):
    """
    Base class for every lead source.
    """

    @abstractmethod
    def search(self, keyword: str) -> List[Lead]:
        """
        Search for leads.

        Example:
            search("Aluminium Extrusion Manufacturers Bangalore")
        """
        pass