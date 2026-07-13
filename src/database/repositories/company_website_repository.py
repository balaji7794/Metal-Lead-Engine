from src.database.database import Database


class CompanyWebsiteRepository:

    def __init__(self):

        self.db = Database()

    def get_all_websites(self):

        self.db.cursor.execute("""

            SELECT
                company_id,
                website

            FROM company_websites

            WHERE website IS NOT NULL
            AND website <> ''

            ORDER BY company_id

        """)

        return self.db.cursor.fetchall()

    def close(self):

        self.db.close()