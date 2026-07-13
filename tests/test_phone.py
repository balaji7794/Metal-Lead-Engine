import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.crawlers.website_crawler import WebsiteCrawler

crawler = WebsiteCrawler()

url = "https://www.flexiprofiles.com"

print(f"\nDownloading: {url}\n")

html = crawler.download(url)

if not html:
    print("Download failed.")
    exit()

phones = crawler.extract_phones(html)

print("\nVALID PHONES")
print("=" * 40)

for phone in phones:
    print(phone)

print("\nTOTAL:", len(phones))