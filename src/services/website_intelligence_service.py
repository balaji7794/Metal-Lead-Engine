from src.database.repositories.company_website_repository import CompanyWebsiteRepository
from src.database.repositories.email_repository import EmailRepository
from src.database.repositories.phone_repository import PhoneRepository
from src.crawlers.website_crawler import WebsiteCrawler


class WebsiteIntelligenceService:

    def __init__(self):

        self.website_repo = CompanyWebsiteRepository()
        self.email_repo = EmailRepository()
        self.phone_repo = PhoneRepository()
        self.crawler = WebsiteCrawler()

    def run(self, company_ids, progress=None):

        websites = self.website_repo.get_websites_by_company_ids(company_ids)

        print()
        print("=" * 60)
        print("WEBSITE INTELLIGENCE")
        print("=" * 60)
        print()

        print(f"Websites Found : {len(websites)}")
        print()

        total = len(websites)

        for index, row in enumerate(websites, start=1):

            company_id = row["company_id"]
            website = row["website"]

            # ----------------------------------------
            # Live Progress
            # ----------------------------------------

            if progress is not None:

                progress["stage"] = "Website Intelligence"
                progress["current"] = index
                progress["total"] = total
                progress["message"] = website

            print(f"[{index}/{total}] {website}")

            html = self.crawler.download(website)

            if not html:
                continue

            all_emails = set()
            all_phones = set()

            # ----------------------------------------
            # Homepage
            # ----------------------------------------

            all_emails.update(

                self.crawler.extract_emails(html)

            )

            all_phones.update(

                self.crawler.extract_phones(html)

            )

            # ----------------------------------------
            # Contact Page Only
            # ----------------------------------------

            pages = self.crawler.discover_pages(

                website,

                html

            )

            print(f"   Contact Pages : {len(pages)}")

            for page in pages:

                if progress is not None:

                    progress["message"] = page

                result = self.crawler.crawl_page(page)

                if not result:
                    continue

                all_emails.update(

                    result["emails"]

                )

                all_phones.update(

                    result["phones"]

                )

            # ----------------------------------------
            # Save Emails
            # ----------------------------------------

            for email in sorted(all_emails):

                self.email_repo.save(

                    company_id,

                    email

                )

            # ----------------------------------------
            # Save Phones
            # ----------------------------------------

            for phone in sorted(all_phones):

                self.phone_repo.save(

                    company_id,

                    phone

                )

            print(f"   Emails : {len(all_emails)}")
            print(f"   Phones : {len(all_phones)}")
            print()

        print("=" * 60)
        print("WEBSITE INTELLIGENCE COMPLETED")
        print("=" * 60)

    def close(self):

        self.website_repo.close()
        self.email_repo.close()
        self.phone_repo.close()