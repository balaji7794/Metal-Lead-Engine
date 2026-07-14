import re

from src.crawlers.product_rules import (

    PRODUCT_CATEGORIES,

    IGNORE_EXACT,

    IGNORE_CONTAINS

)


class ProductScorer:

    def __init__(self):

        pass

    def score(self, text):

        if not text:

            return 0

        text = text.strip()

        lower = text.lower()

        # ------------------------
        # Immediate Reject
        # ------------------------

        if lower in IGNORE_EXACT:

            return 0

        for word in IGNORE_CONTAINS:

            if word in lower:

                return 0

        score = 0

        # ------------------------
        # Product Keyword
        # ------------------------

        for keyword in PRODUCT_CATEGORIES:

            if keyword in lower:

                score += 50
                break

        # ------------------------
        # Aluminium Mention
        # ------------------------

        if "aluminium" in lower:

            score += 20

        if "aluminum" in lower:

            score += 20

        # ------------------------
        # Length
        # ------------------------

        words = len(lower.split())

        if 2 <= words <= 6:

            score += 20

        elif 7 <= words <= 10:

            score += 10

        elif words > 15:

            score -= 40

        # ------------------------
        # Sentence Detection
        # ------------------------

        if lower.endswith("."):

            score -= 20

        if ";" in lower:

            score -= 30

        if ":" in lower:

            score -= 20

        # ------------------------
        # Email / URL
        # ------------------------

        if re.search(r"@", lower):

            return 0

        if re.search(r"http", lower):

            return 0

        if re.search(r"www", lower):

            return 0

        # ------------------------
        # Digits only
        # ------------------------

        if re.fullmatch(r"[0-9\-\+\s]+", lower):

            return 0

        return max(score, 0)