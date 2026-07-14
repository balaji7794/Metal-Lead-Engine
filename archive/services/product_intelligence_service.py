from src.database.repositories.company_website_repository import CompanyWebsiteRepository
from src.database.repositories.product_repository import ProductRepository

from src.crawlers.website_crawler import WebsiteCrawler
from src.crawlers.product_extractor import ProductExtractor


class ProductIntelligenceService:

    def __init__(self):

        self.website_repo = CompanyWebsiteRepository()
        self.product_repo = ProductRepository()

        self.website_crawler = WebsiteCrawler()
        self.product_extractor = ProductExtractor()

    def run(self):

        websites = self.website_repo.get_all_websites()

        print()
        print("=" * 60)
        print("PRODUCT INTELLIGENCE")
        print("=" * 60)
        print()

        print(f"Websites Found : {len(websites)}")
        print()

        for index, row in enumerate(websites, start=1):

            company_id = row["company_id"]
            website = row["website"]

            print(f"[{index}/{len(websites)}] {website}")

            html = self.website_crawler.download(website)

            if not html:
                continue

            products = []

            # --------------------------------
            # Homepage
            # --------------------------------

            products.extend(

                self.product_extractor.extract(

                    html

                )

            )

            # --------------------------------
            # Important Pages
            # --------------------------------

            pages = self.website_crawler.discover_pages(

                website,

                html

            )

            for page in pages:

                result = self.website_crawler.crawl_page(page)

                if not result:
                    continue

                products.extend(

                    self.product_extractor.extract(

                        result["html"]

                    )

                )

            # --------------------------------
            # Remove Duplicates
            # --------------------------------

            unique = {}

            for product in products:

                key = (

                    product["product_name"].lower(),

                    product["grade"]

                )

                unique[key] = product

            print(f"   Products : {len(unique)}")

            # --------------------------------
            # Save Products
            # --------------------------------

            for product in sorted(

                unique.values(),

                key=lambda x: (

                    x["product_name"],

                    x["grade"]

                )

            ):

                self.product_repo.save(

                    company_id,

                    product["product_name"],

                    product["category"],

                    product["grade"],

                    product["confidence"]

                )

            print()

        print("=" * 60)
        print("PRODUCT INTELLIGENCE COMPLETED")
        print("=" * 60)

    def close(self):

        self.website_repo.close()
        self.product_repo.close()