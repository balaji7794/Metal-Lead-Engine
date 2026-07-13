from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Lead:

    # Basic Information
    name: str = ""
    category: str = ""

    # Location
    address: str = ""
    city: str = ""
    state: str = ""
    country: str = ""

    # Contact
    phone: str = ""
    website: str = ""
    emails: List[str] = field(default_factory=list)

    # Maps
    google_maps_url: str = ""

    # Reviews
    rating: Optional[float] = None
    review_count: int = 0

    # Coordinates
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Source
    source: str = "Google Maps"

    # Classification
    company_type: str = ""
    confidence: float = 0.0

    # Future
    gst: str = ""
    contact_person: str = ""
    designation: str = ""

    notes: str = ""