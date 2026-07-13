import re
import urllib3
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebsiteCrawler:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",

            "Accept-Language": "en-US,en;q=0.9",

            "Connection": "keep-alive"

        })

        self.blocked_domains = {

            "sentry.io",
            "wixpress.com",
            "wix.com",
            "example.com",
            "latofonts.com"

        }

        self.blocked_words = {

            "sentry",
            "wixpress",
            "example@",
            "noreply",
            "no-reply",
            "donotreply",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".webp",
            ".css",
            ".js",
            ".woff",
            ".ttf"

        }

        self.priority_keywords = [

            "contact",
            "contact-us",
            "about",
            "about-us",
            "reach",
            "location",
            "locations",
            "company",
            "profile",
            "infrastructure"

        ]

        self.ignore_keywords = [

            "product",
            "products",
            "category",
            "catalog",
            "shop",
            "cart",
            "gallery",
            "portfolio",
            "blog",
            "news",
            "career",
            "job",
            "privacy",
            "terms"

        ]

    def download(self, url):

        for verify in [True, False]:

            try:

                response = self.session.get(

                    url,

                    timeout=20,

                    verify=verify,

                    allow_redirects=True

                )

                response.raise_for_status()

                print("✅ Website Downloaded")

                return response.text

            except:

                continue

        print("❌ Failed")

        return None

    def extract_emails(self, html):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        emails = set()

        for email in re.findall(pattern, html):

            email = email.strip().lower()

            if self.is_valid_email(email):

                emails.add(email)

        return sorted(emails)

    def extract_phones(self, html):

        phones = set()

        patterns = [

            r'\+91[\s\-]?[6-9]\d{9}',
            r'\b91[6-9]\d{9}\b',
            r'\b[6-9]\d{9}\b',
            r'\b0\d{2,4}[\-\s]?\d{6,8}\b'

        ]

        for pattern in patterns:

            matches = re.findall(pattern, html)

            for phone in matches:

                original = phone

                digits = re.sub(r"\D", "", phone)

                # -------------------------
                # Normalize
                # -------------------------

                if digits.startswith("91") and len(digits) == 12:

                    digits = digits[2:]

                    original = "+91" + digits

                elif len(digits) == 10:

                    original = digits

                elif digits.startswith("0"):

                    original = digits

                # -------------------------
                # Validation
                # -------------------------

                if len(set(digits)) == 1:
                    continue

                if digits.startswith("000"):
                    continue

                if digits.startswith("123"):
                    continue

                if len(digits) == 10:

                    if digits[0] not in "6789":
                        continue

                elif len(digits) == 11:

                    if not digits.startswith("0"):
                        continue

                else:
                    continue

                # Reject sequential numbers

                if digits in {

                    "9876543210",
                    "1234567890"

                }:
                    continue

                phones.add(original)

        return sorted(phones)

    def is_valid_email(self, email):

        for word in self.blocked_words:

            if word in email:

                return False

        domain = email.split("@")[-1]

        if domain in self.blocked_domains:

            return False

        tld = domain.split(".")[-1]

        if len(tld) < 2:

            return False

        return True

    def discover_pages(self, base_url, html):

        soup = BeautifulSoup(html, "lxml")

        pages = []

        for a in soup.find_all("a", href=True):

            href = a.get("href", "").strip()

            if not href:

                continue

            href = href.split("#")[0]

            text = a.get_text(" ", strip=True).lower()

            value = (href + " " + text).lower()

            if any(word in value for word in self.ignore_keywords):

                continue

            if not any(word in value for word in self.priority_keywords):

                continue

            url = urljoin(base_url, href)

            if not url.startswith("http"):

                continue

            if url not in pages:

                pages.append(url)

        return pages[:5]

    def crawl_page(self, url):

        html = self.download(url)

        if not html:

            return None

        return {

            "url": url,

            "emails": self.extract_emails(html),

            "phones": self.extract_phones(html),

            "html": html

        }