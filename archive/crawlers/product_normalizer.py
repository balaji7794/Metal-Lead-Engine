import re

from src.crawlers.product_rules import GRADE_REGEX


class ProductNormalizer:

    def __init__(self):

        self.grade_pattern = re.compile(

            GRADE_REGEX,

            re.IGNORECASE

        )

        self.replacements = {

            "profiles": "profile",
            "sheets": "sheet",
            "plates": "plate",
            "coils": "coil",
            "bars": "bar",
            "rods": "rod",
            "tubes": "tube",
            "pipes": "pipe",
            "ingots": "ingot",
            "billets": "billet",
            "castings": "casting",
            "heat sinks": "heat sink",
            "bus bars": "bus bar"

        }

    def normalize(self, text):

        if not text:

            return "", ""

        text = re.sub(

            r"\s+",

            " ",

            text

        ).strip()

        grade = ""

        match = self.grade_pattern.search(text)

        if match:

            grade = (

                match.group(1)

                .upper()

                .replace(" ", "")

                .replace("-", "")

            )

            text = self.grade_pattern.sub(

                "",

                text

            )

        text = text.lower()

        for old, new in self.replacements.items():

            text = re.sub(

                rf"\b{re.escape(old)}\b",

                new,

                text

            )

        text = re.sub(

            r"\s+",

            " ",

            text

        ).strip(" -")

        text = " ".join(

            word.capitalize()

            for word in text.split()

        )

        return text, grade