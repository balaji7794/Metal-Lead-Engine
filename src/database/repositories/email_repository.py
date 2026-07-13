from src.database.database import Database


class EmailRepository:

    def __init__(self):

        self.db = Database()

    def save(self, company_id, email):

        if not email:
            return

        email = email.strip().lower()

        # Ignore obvious junk emails

        blocked = [

            "sentry",

            "wixpress",

            "example@",

            ".jpg",

            ".jpeg",

            ".png",

            ".svg",

            ".webp",

            "font"

        ]

        for word in blocked:

            if word in email:

                return

        self.db.cursor.execute("""

        SELECT id

        FROM company_emails

        WHERE company_id=?

        AND LOWER(email)=?

        """, (

            company_id,

            email

        ))

        if self.db.cursor.fetchone():

            return

        self.db.cursor.execute("""

        INSERT INTO company_emails(

            company_id,

            email,

            department,

            is_primary,

            verified

        )

        VALUES(?,?,?,?,?)

        """, (

            company_id,

            email,

            "General",

            0,

            0

        ))

        self.db.conn.commit()

        print(f"      ✓ Saved : {email}")

    def close(self):

        self.db.close()