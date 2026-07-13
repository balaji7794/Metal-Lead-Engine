from src.database.repositories.company_repository import CompanyRepository
from src.database.repositories.phone_repository import PhoneRepository
from src.database.repositories.website_repository import WebsiteRepository
from src.database.repositories.email_repository import EmailRepository


class LeadService:

    def __init__(self):

        self.company_repo = CompanyRepository()
        self.phone_repo = PhoneRepository()
        self.website_repo = WebsiteRepository()
        self.email_repo = EmailRepository()

    def save(self, leads):

        new_companies = 0
        updated_companies = 0

        for lead in leads:

            company_id, is_new = self.company_repo.save(lead)

            if is_new:
                new_companies += 1
            else:
                updated_companies += 1

            # ---------- Phones ----------

            if lead.phone:

                phones = []

                for phone in lead.phone.replace(";", ",").split(","):

                    phone = phone.strip()

                    if phone:

                        phones.append(phone)

                for index, phone in enumerate(phones):

                    self.phone_repo.save(
                        company_id,
                        phone,
                        "Office",
                        index == 0
                    )

            # ---------- Website ----------

            if lead.website:

                self.website_repo.save(
                    company_id,
                    lead.website
                )

            # ---------- Emails ----------

            for email in lead.emails:

                self.email_repo.save(
                    company_id,
                    email
                )

        print("\n==============================")
        print("DATABASE SUMMARY")
        print("==============================")
        print(f"New Companies     : {new_companies}")
        print(f"Updated Companies : {updated_companies}")
        print("==============================")

    def close(self):

        self.company_repo.close()