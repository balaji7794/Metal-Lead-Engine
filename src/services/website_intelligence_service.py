from src.database.repositories.company_website_repository import CompanyWebsiteRepository
from src.database.repositories.email_repository import EmailRepository
from src.crawlers.website_crawler import WebsiteCrawler


class WebsiteIntelligenceService:

    def __init__(self):

        self.website_repo = CompanyWebsiteRepository()
        self.email_repo = EmailRepository()
        self.crawler = WebsiteCrawler()

    def run(self):

        websites = self.website_repo.get_all_websites()

        print(f"\nWebsites Found : {len(websites)}\n")

        for row in websites:

            company_id = row["company_id"]
            website = row["website"]

            print(f"Crawling : {website}")

            html = self.crawler.download(website)

            if not html:
                continue

            emails = self.crawler.extract_emails(html)

            for email in emails:

                self.email_repo.save(
                    company_id,
                    email
                )

                print(f"   + {email}")

        print("\n✅ Website Intelligence Completed")

    def close(self):

        self.website_repo.close()