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

    def run(self):

        websites = self.website_repo.get_all_websites()

        print("\n" + "=" * 60)
        print("WEBSITE INTELLIGENCE")
        print("=" * 60)

        print(f"\nWebsites Found : {len(websites)}\n")

        for index, row in enumerate(websites, start=1):

            company_id = row["company_id"]
            website = row["website"]

            print(f"[{index}/{len(websites)}] {website}")

            html = self.crawler.download(website)

            if not html:
                continue

            all_emails = set()
            all_phones = set()

            # -----------------------------
            # Homepage
            # -----------------------------

            all_emails.update(

                self.crawler.extract_emails(html)

            )

            all_phones.update(

                self.crawler.extract_phones(html)

            )

            # -----------------------------
            # Important Pages
            # -----------------------------

            pages = self.crawler.discover_pages(

                website,

                html

            )

            print(f"   Important Pages : {len(pages)}")

            for page in pages:

                result = self.crawler.crawl_page(page)

                if not result:
                    continue

                all_emails.update(

                    result["emails"]

                )

                all_phones.update(

                    result["phones"]

                )

            # -----------------------------
            # Save Emails
            # -----------------------------

            email_count = 0

            for email in sorted(all_emails):

                self.email_repo.save(

                    company_id,

                    email

                )

                email_count += 1

            # -----------------------------
            # Save Phones
            # -----------------------------

            phone_count = 0

            for phone in sorted(all_phones):

                self.phone_repo.save(

                    company_id,

                    phone

                )

                phone_count += 1

            print(f"   Emails : {email_count}")
            print(f"   Phones : {phone_count}")

            if email_count:

                print("\n   EMAILS")

                for email in sorted(all_emails):

                    print(f"      • {email}")

            if phone_count:

                print("\n   PHONES")

                for phone in sorted(all_phones):

                    print(f"      • {phone}")

            print()

        print("=" * 60)
        print("WEBSITE INTELLIGENCE COMPLETED")
        print("=" * 60)

    def close(self):

        self.website_repo.close()
        self.email_repo.close()
        self.phone_repo.close()