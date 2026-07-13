from typing import List

from src.engines.engine_base import EngineBase
from src.models.lead import Lead


class GoogleMapsEngine(EngineBase):

    def search(self, keyword: str) -> List[Lead]:
        print(f"Searching Google Maps for: {keyword}")

        # Temporary dummy data
        return [
            Lead(
                name="ABC Aluminium Pvt Ltd",
                category="Aluminium Extrusion",
                city="Bangalore",
                source="Google Maps",
            )
        ]