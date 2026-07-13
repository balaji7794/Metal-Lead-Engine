from src.database.database import Database


class WebsiteRepository:

    def __init__(self):

        self.db = Database()

    def save(self, company_id, website):

        if not website:
            return

        self.db.cursor.execute("""

        SELECT id

        FROM company_websites

        WHERE company_id=?

        AND website=?

        """,(company_id, website))

        if self.db.cursor.fetchone():
            return

        self.db.cursor.execute("""

        INSERT INTO company_websites(

            company_id,

            website,

            website_type,

            is_primary

        )

        VALUES(?,?,?,?)

        """,(

            company_id,

            website,

            "Corporate",

            1

        ))

        self.db.conn.commit()