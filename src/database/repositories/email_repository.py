from src.database.database import Database


class EmailRepository:

    def __init__(self):

        self.db = Database()

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, company_id, email):

        if not email:
            return

        email = email.strip().lower()

        blocked = {

            "sentry",
            "wixpress",
            "example@",
            ".jpg",
            ".jpeg",
            ".png",
            ".svg",
            ".webp",
            "font"

        }

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

        print(f"      ✓ Email Saved : {email}")

    # =====================================================
    # READ
    # =====================================================

    def get_by_company(self, company_id):

        self.db.cursor.execute("""

        SELECT *

        FROM company_emails

        WHERE company_id=?

        ORDER BY

            is_primary DESC,

            email

        """, (

            company_id,

        ))

        return self.db.cursor.fetchall()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, email_id):

        self.db.cursor.execute("""

        DELETE FROM company_emails

        WHERE id=?

        """, (

            email_id,

        ))

        self.db.conn.commit()

    # =====================================================
    # PRIMARY
    # =====================================================

    def set_primary(self, company_id, email_id):

        self.db.cursor.execute("""

        UPDATE company_emails

        SET is_primary=0

        WHERE company_id=?

        """, (

            company_id,

        ))

        self.db.cursor.execute("""

        UPDATE company_emails

        SET is_primary=1

        WHERE id=?

        """, (

            email_id,

        ))

        self.db.conn.commit()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.db.close()