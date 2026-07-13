import re

from bs4 import BeautifulSoup

from src.crawlers.product_rules import PRODUCT_CATEGORIES
from src.crawlers.product_normalizer import ProductNormalizer
from src.crawlers.product_classifier import ProductClassifier


class ProductExtractor:

    def __init__(self):

        self.normalizer = ProductNormalizer()
        self.classifier = ProductClassifier()

        self.tags = [

            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "li",
            "strong",
            "b",
            "td",
            "th",
            "span"

        ]

    def detect_category(self, product_name):

        lower = product_name.lower()

        # Long sentences are never products
        if len(lower.split()) > 8:
            return ""

        for keyword, category in PRODUCT_CATEGORIES.items():

            if keyword in lower:

                return category

        return ""

    def extract(self, html):

        soup = BeautifulSoup(html, "lxml")

        products = []

        seen = set()

        for tag in self.tags:

            for item in soup.find_all(tag):

                text = item.get_text(" ", strip=True)

                text = re.sub(r"\s+", " ", text).strip()

                if not text:
                    continue

                if len(text) < 3:
                    continue

                if len(text) > 80:
                    continue

                classification, confidence = self.classifier.classify(text)

                # Keep only actual products and accessories
                if classification not in (

                    ProductClassifier.PRODUCT,
                    ProductClassifier.ACCESSORY

                ):
                    continue

                product_name, grade = self.normalizer.normalize(text)

                if not product_name:
                    continue

                category = self.detect_category(product_name)

                if not category:
                    continue

                key = (

                    product_name.lower(),

                    grade

                )

                if key in seen:
                    continue

                seen.add(key)

                products.append({

                    "product_name": product_name,

                    "grade": grade,

                    "category": category,

                    "confidence": confidence

                })

        return products