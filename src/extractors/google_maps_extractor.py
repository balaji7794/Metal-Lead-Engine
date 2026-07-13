import re

from src.models.lead import Lead


class GoogleMapsExtractor:

    def __init__(self, page):
        self.page = page

    def _text(self, locator):
        try:
            if locator.count() > 0:
                return locator.first.inner_text().strip()
        except Exception:
            pass

        return ""

    def _clean(self, text):

        if not text:
            return ""

        for ch in ["", "", "", "", ""]:
            text = text.replace(ch, "")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract(self):

        lead = Lead()

        # -------------------------
        # NAME
        # -------------------------

        lead.name = self._clean(
            self._text(
                self.page.locator("h1.DUwDvf")
            )
        )

        # -------------------------
        # CATEGORY
        # -------------------------

        try:

            category = self.page.locator(
                'button[jsaction*="pane.rating.category"]'
            )

            if category.count():

                lead.category = self._clean(
                    category.first.inner_text()
                )

        except Exception:
            pass

        # -------------------------
        # ADDRESS
        # -------------------------

        try:

            address = self.page.locator(
                'button[data-item-id="address"]'
            )

            if address.count():

                lead.address = self._clean(
                    address.first.inner_text()
                )

        except Exception:
            pass

        # -------------------------
        # PHONE
        # -------------------------

        try:

            phone = self.page.locator(
                'button[data-item-id^="phone"]'
            )

            if phone.count():

                lead.phone = self._clean(
                    phone.first.inner_text()
                )

        except Exception:
            pass

        # -------------------------
        # WEBSITE
        # -------------------------

        try:

            website = self.page.locator(
                'a[data-item-id="authority"]'
            )

            if website.count():

                lead.website = (
                    website.first.get_attribute("href") or ""
                )

        except Exception:
            pass

        # -------------------------
        # RATING
        # -------------------------

        try:

            rating = self.page.locator(
                'div[role="img"][aria-label*="star"]'
            )

            if rating.count():

                txt = rating.first.get_attribute("aria-label")

                if txt:

                    m = re.search(r"([0-9.]+)", txt)

                    if m:
                        lead.rating = float(m.group(1))

        except Exception:
            pass

        # -------------------------
        # REVIEW COUNT
        # -------------------------

        try:

            review_button = self.page.locator(
                'button[jsaction*="pane.reviewChart.moreReviews"]'
            )

            if review_button.count():

                txt = review_button.first.inner_text()

                m = re.search(r"([0-9,]+)", txt)

                if m:

                    lead.review_count = int(
                        m.group(1).replace(",", "")
                    )

        except Exception:
            pass

        lead.source = "Google Maps"

        return lead