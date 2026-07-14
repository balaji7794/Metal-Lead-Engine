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
            "overview", "tips", "blog", "article",
            "learn", "selecting", "selection", "choosing"
        }

        self.process_words = {
            "heat", "cool", "cut", "drill", "machine",
            "homogenise", "homogenize", "extrude",
            "pack", "bundle", "protect",
            "load", "unload", "furnace",
            "welding", "fabrication", "assembly"
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
            "mission",
            "factsheet",
            "testimonial",
            "careers"
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
            "top",
            "buy",
            "sale"
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

        self.reject_contains = {
            "@",
            "http://",
            "https://",
            "www.",
            "youtube",
            "gallery",
            "download",
            "catalogue",
            "catalog",
            "brochure",
            "pdf",
            "read more",
            "click here",
            "visit",
            "login",
            "register",
            "privacy",
            "terms",
            "cookie",
            "news",
            "events"
        }

    def classify(self, text):

        if not text:
            return self.UNKNOWN, 0

        text = re.sub(r"\s+", " ", text).strip()
        lower = text.lower()

        # -------------------------
        # Hard Reject
        # -------------------------

        for word in self.reject_contains:
            if word in lower:
                return self.UNKNOWN, 0

        if re.fullmatch(r"[0-9+\-\s]+", lower):
            return self.UNKNOWN, 0

        words = lower.split()

        if len(words) == 1:
            if words[0] in {
                "products",
                "profile",
                "profiles",
                "home",
                "about",
                "contact"
            }:
                return self.UNKNOWN, 0

        score = {
            self.PRODUCT: 0,
            self.ACCESSORY: 0,
            self.PROCESS: 0,
            self.ARTICLE: 0,
            self.COMPANY: 0,
            self.CONTACT: 0,
            self.SEO: 0
        }

        # Product

        for word in self.product_words:
            if word in lower:
                score[self.PRODUCT] += 50

        # Accessory

        for word in self.accessory_words:
            if word in lower:
                score[self.ACCESSORY] += 45

        # Process

        for word in self.process_words:
            if word in lower:
                score[self.PROCESS] += 45

        # Article

        for word in self.article_words:
            if word in lower:
                score[self.ARTICLE] += 45

        # Company

        for word in self.company_words:
            if word in lower:
                score[self.COMPANY] += 45

        # Contact

        for word in self.contact_words:
            if word in lower:
                score[self.CONTACT] += 45

        # SEO

        for word in self.seo_words:
            if word in lower:
                score[self.SEO] += 45

        # Positive signals

        if "aluminium" in lower or "aluminum" in lower:
            score[self.PRODUCT] += 15

        if 2 <= len(words) <= 6:
            score[self.PRODUCT] += 20

        if len(words) > 10:
            score[self.ARTICLE] += 20

        if ":" in lower:
            score[self.ARTICLE] += 20

        if ";" in lower:
            score[self.ARTICLE] += 20

        # Priority overrides

        if score[self.ARTICLE] >= 45:
            return self.ARTICLE, score[self.ARTICLE]

        if score[self.PROCESS] >= 45:
            return self.PROCESS, score[self.PROCESS]

        if score[self.COMPANY] >= 45:
            return self.COMPANY, score[self.COMPANY]

        if score[self.CONTACT] >= 45:
            return self.CONTACT, score[self.CONTACT]

        if score[self.SEO] >= 45 and score[self.PRODUCT] < 70:
            return self.SEO, score[self.SEO]

        if score[self.ACCESSORY] >= 45:
            return self.ACCESSORY, min(score[self.ACCESSORY], 100)

        if score[self.PRODUCT] >= 60:
            return self.PRODUCT, min(score[self.PRODUCT], 100)

        return self.UNKNOWN, 0