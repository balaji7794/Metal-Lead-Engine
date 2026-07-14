from src.database.database import Database


class CompanyWebsiteRepository:

    def __init__(self):

        self.db = Database()

    def get_websites_by_company_ids(self, company_ids):

        if not company_ids:
            return []

        placeholders = ",".join(["?"] * len(company_ids))

        query = f"""

            SELECT
                company_id,
                website

            FROM company_websites

            WHERE company_id IN ({placeholders})

            AND website IS NOT NULL
            AND website <> ''

            ORDER BY company_id

        """

        self.db.cursor.execute(

            query,

            company_ids

        )

        return self.db.cursor.fetchall()

    def close(self):

        self.db.close()