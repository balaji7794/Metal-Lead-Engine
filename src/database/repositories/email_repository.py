from src.database.database import Database


class EmailRepository:

    def __init__(self):

        self.db = Database()

    def save(self, company_id, email):

        if not email:
            return

        self.db.cursor.execute("""

        SELECT id

        FROM company_emails

        WHERE company_id=?

        AND email=?

        """,(company_id, email))

        if self.db.cursor.fetchone():
            return

        self.db.cursor.execute("""

        INSERT INTO company_emails(

            company_id,

            email,

            department,

            is_primary

        )

        VALUES(?,?,?,?)

        """,(

            company_id,

            email,

            "General",

            1

        ))

        self.db.conn.commit()