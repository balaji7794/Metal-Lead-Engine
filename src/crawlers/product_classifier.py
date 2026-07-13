import re


class ProductClassifier:

    PRODUCT = "PRODUCT"
    ACCESSORY = "ACCESSORY"
    PROCESS = "PROCESS"
    ARTICLE = "ARTICLE"
    COMPANY = "COMPANY"
    CONTACT = "CONTACT"
    SEO = "SEO"
    UNKNOWN = "UNKNOWN"

    def __init__(self):

        self.article_words = {
            "how", "why", "benefits", "advantage", "advantages",
            "application", "applications", "guide", "introduction",
            "overview", "tips", "blog", "article"
        }

        self.process_words = {
            "heat", "cool", "cut", "drill", "machine",
            "homogenise", "homogenize", "extrude",
            "pack", "bundle", "protect",
            "load", "unload", "furnace"
        }

        self.contact_words = {
            "contact", "call", "mobile", "phone",
            "email", "whatsapp", "address", "location"
        }

        self.company_words = {
            "company",
            "about us",
            "our company",
            "our profile",
            "company profile",
            "history",
            "vision",
            "mission"
        }

        self.seo_words = {
            "manufacturer",
            "manufacturers",
            "supplier",
            "suppliers",
            "exporter",
            "exporters",
            "dealer",
            "dealers",
            "distributor",
            "distributors",
            "near me",
            "best",
            "top"
        }

        self.product_words = {
            "profile",
            "sheet",
            "plate",
            "coil",
            "foil",
            "strip",
            "pipe",
            "tube",
            "rod",
            "bar",
            "billet",
            "ingot",
            "casting",
            "heat sink",
            "bus bar"
        }

        self.accessory_words = {
            "bracket",
            "corner",
            "connector",
            "joint",
            "clamp",
            "hinge",
            "accessory",
            "accessories",
            "fastener",
            "bolt",
            "nut",
            "screw"
        }

    def classify(self, text):

        if not text:
            return self.UNKNOWN, 0

        text = text.strip()
        lower = text.lower()

        # -----------------------------
        # Hard Rejects
        # -----------------------------

        if "@" in lower:
            return self.CONTACT, 0

        if "http://" in lower or "https://" in lower:
            return self.CONTACT, 0

        if "www." in lower:
            return self.CONTACT, 0

        if re.fullmatch(r"[0-9+\-\s]+", lower):
            return self.CONTACT, 0

        scores = {
            self.PRODUCT: 0,
            self.ACCESSORY: 0,
            self.PROCESS: 0,
            self.ARTICLE: 0,
            self.COMPANY: 0,
            self.CONTACT: 0,
            self.SEO: 0
        }

        # -----------------------------
        # Word Scores
        # -----------------------------

        for word in self.product_words:
            if word in lower:
                scores[self.PRODUCT] += 50

        for word in self.accessory_words:
            if word in lower:
                scores[self.ACCESSORY] += 45

        for word in self.process_words:
            if word in lower:
                scores[self.PROCESS] += 40

        for word in self.article_words:
            if word in lower:
                scores[self.ARTICLE] += 40

        for word in self.company_words:
            if word in lower:
                scores[self.COMPANY] += 40

        for word in self.contact_words:
            if word in lower:
                scores[self.CONTACT] += 40

        for word in self.seo_words:
            if word in lower:
                scores[self.SEO] += 45

        # -----------------------------
        # Positive Signals
        # -----------------------------

        if "aluminium" in lower or "aluminum" in lower:
            scores[self.PRODUCT] += 15

        words = len(lower.split())

        if 2 <= words <= 6:
            scores[self.PRODUCT] += 20

        elif words > 12:
            scores[self.ARTICLE] += 20

        if ":" in lower:
            scores[self.ARTICLE] += 15

        if ";" in lower:
            scores[self.ARTICLE] += 20

        # -----------------------------
        # Decide Winner
        # -----------------------------

        winner = max(scores, key=scores.get)
        confidence = scores[winner]

        if confidence < 40:
            return self.UNKNOWN, confidence

        return winner, min(confidence, 100)