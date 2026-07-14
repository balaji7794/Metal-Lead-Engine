from playwright.sync_api import sync_playwright

from src.extractors.google_maps_extractor import GoogleMapsExtractor


class GoogleMapsScraper:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu"
            ]
        )

        self.page = self.browser.new_page(
            viewport={"width":1600,"height":900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/138.0.0.0 Safari/537.36"
        )

    def search(self, keyword):

        print(f"\nSearching : {keyword}")

        self.page.goto(
            "https://www.google.com/maps",
            wait_until="domcontentloaded"
        )

        self.page.wait_for_timeout(5000)

        self.page.locator(
            'input[name="q"]'
        ).fill(keyword)

        self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(7000)

    def load_all_results(self):

        print("\nLoading all Google Maps results...\n")

        panel = self.page.locator('div[role="feed"]')

        previous = -1

        while True:

            companies = self.page.locator(
                'a[href*="/place/"]'
            )

            current = companies.count()

            print(f"Loaded : {current}")

            if current == previous:
                break

            previous = current

            try:
                panel.evaluate(
                    "(e)=>e.scrollBy(0,3000)"
                )
            except:
                break

            self.page.wait_for_timeout(2500)

        print(f"\nFinished loading {previous} companies.\n")

    def scrape_all(self):

        self.load_all_results()

        print("Collecting unique company URLs...\n")

        companies = self.page.locator(
            'a[href*="/place/"]'
        )

        urls = []
        visited = set()

        total = companies.count()

        for i in range(total):

            try:

                href = companies.nth(i).get_attribute("href")

                if not href:
                    continue

                if "/place/" not in href:
                    continue

                href = href.split("&")[0]

                if href in visited:
                    continue

                visited.add(href)

                urls.append(href)

            except Exception:
                continue

        print(f"Unique Companies : {len(urls)}\n")

        extractor = GoogleMapsExtractor(self.page)

        leads = []

        for index, url in enumerate(urls):

            print(f"Scraping {index+1}/{len(urls)}")

            self.page.goto(
                url,
                wait_until="domcontentloaded"
            )

            self.page.wait_for_timeout(3500)

            lead = extractor.extract()

            lead.google_maps_url = url

            leads.append(lead)

            print(f"✓ {lead.name}")

        return leads

    def stop(self):

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()