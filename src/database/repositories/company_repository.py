from src.database.database import Database


class CompanyRepository:

    def __init__(self):

        self.db = Database()

    def get_by_maps_url(self, maps_url):

        self.db.cursor.execute(
            "SELECT * FROM companies WHERE google_maps_url=?",
            (maps_url,)
        )

        return self.db.cursor.fetchone()

    def insert(self, lead):

        self.db.insert_company(lead)

        self.db.cursor.execute(
            "SELECT id FROM companies WHERE google_maps_url=?",
            (lead.google_maps_url,)
        )

        row = self.db.cursor.fetchone()

        return row["id"]

    def update(self, lead):

        self.db.update_company(lead)

        self.db.cursor.execute(
            "SELECT id FROM companies WHERE google_maps_url=?",
            (lead.google_maps_url,)
        )

        row = self.db.cursor.fetchone()

        return row["id"]

    def save(self, lead):

        company = self.get_by_maps_url(lead.google_maps_url)

        if company:

            self.update(lead)

            return company["id"], False

        company_id = self.insert(lead)

        return company_id, True

    def close(self):

        self.db.close()