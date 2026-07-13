from src.database.database import Database


class PhoneRepository:

    def __init__(self):

        self.db = Database()

    def save(self, company_id, phone, phone_type="Office", is_primary=True):

        if not phone:
            return

        self.db.cursor.execute("""

        SELECT id

        FROM company_phones

        WHERE company_id=?

        AND phone=?

        """, (company_id, phone))

        if self.db.cursor.fetchone():
            return

        self.db.cursor.execute("""

        INSERT INTO company_phones(

            company_id,

            phone,

            phone_type,

            is_primary

        )

        VALUES(?,?,?,?)

        """,(

            company_id,

            phone,

            phone_type,

            1 if is_primary else 0

        ))

        self.db.conn.commit()   