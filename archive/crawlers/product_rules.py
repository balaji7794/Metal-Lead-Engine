# =====================================================
# PRODUCT RULES
# =====================================================

PRODUCT_CATEGORIES = {

    # Extrusion

    "profile": "Extrusion",
    "profiles": "Extrusion",
    "heat sink": "Extrusion",
    "heat sinks": "Extrusion",
    "t-slot": "Extrusion",
    "t slot": "Extrusion",
    "solar profile": "Extrusion",
    "window profile": "Extrusion",
    "door profile": "Extrusion",
    "partition profile": "Extrusion",
    "architectural profile": "Extrusion",
    "industrial profile": "Extrusion",

    # Rolled Products

    "sheet": "Rolled Product",
    "sheets": "Rolled Product",
    "coil": "Rolled Product",
    "coils": "Rolled Product",
    "plate": "Rolled Product",
    "plates": "Rolled Product",
    "foil": "Rolled Product",
    "strip": "Rolled Product",
    "chequered sheet": "Rolled Product",

    # Bars

    "flat bar": "Bar",
    "flat bars": "Bar",
    "round bar": "Bar",
    "round bars": "Bar",
    "square bar": "Bar",
    "square bars": "Bar",
    "hex bar": "Bar",
    "hex bars": "Bar",

    # Tube

    "tube": "Tube",
    "tubes": "Tube",
    "pipe": "Pipe",
    "pipes": "Pipe",

    # Billets

    "billet": "Billet",
    "billets": "Billet",

    # Ingots

    "ingot": "Ingot",
    "ingots": "Ingot",
    "alloy ingot": "Ingot",
    "remelt ingot": "Ingot",

    # Electrical

    "bus bar": "Electrical",
    "bus bars": "Electrical",

    # Casting

    "casting": "Casting",
    "castings": "Casting"

}

# -----------------------------------------------------

IGNORE_EXACT = {

    "product",
    "products",
    "our products",
    "company profile",
    "our profile",
    "view more",
    "view more products",
    "gallery",
    "latest gallery",
    "youtube",
    "our youtube channel",
    "download",
    "brochure",
    "catalogue",
    "factsheet",
    "contact",
    "home",
    "about",
    "services"

}

# -----------------------------------------------------

IGNORE_CONTAINS = [

    "@",

    "http",

    "https",

    "www.",

    "call us",

    "contact us",

    "telephone",

    "mobile",

    "email",

    "whatsapp",

    "read more",

    "rated",

    "benefits",

    "applications",

    "why choose",

    "learn more",

    "click here",

    "our supplier",

    "latest",

    "quality",

    "welcome"

]

# -----------------------------------------------------

GRADE_REGEX = (

    r"\b("

    r"\d{4}|"

    r"ADC\s?-?\d+|"

    r"LM\s?-?\d+|"

    r"A\d{3}|"

    r"AA\d{4}|"

    r"6061|6063|6082|7075"

    r")\b"

)