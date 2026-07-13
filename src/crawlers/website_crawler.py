import re
import requests
from bs4 import BeautifulSoup


class WebsiteCrawler:

    def download(self, url):

        try:

            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

            print("✅ Website Downloaded")

            return response.text

        except Exception as e:

            print(f"\n❌ {e}")

            return None

    def extract_emails(self, html):

        emails = set()

        matches = re.findall(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            html

        )

        for email in matches:

            emails.add(email.lower())

        return sorted(emails)