from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Lead:
    name: str
    category: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    country: str = ""

    phone: str = ""
    website: str = ""

    emails: List[str] = field(default_factory=list)

    google_maps_url: str = ""

    rating: Optional[float] = None
    review_count: int = 0

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    source: str = ""

    notes: str = ""