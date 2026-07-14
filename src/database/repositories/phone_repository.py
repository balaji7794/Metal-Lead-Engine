import re

from src.database.database import Database


class PhoneRepository:

    def __init__(self):

        self.db = Database()

    # =====================================================
    # CLEAN
    # =====================================================

    def clean_phone(self, phone):

        if not phone:
            return None

        digits = re.sub(r"\D", "", phone)

        # Mobile

        if len(digits) == 10:

            if digits[0] in "6789":

                return "+91" + digits

            return None

        # +91

        if len(digits) == 12 and digits.startswith("91"):

            return "+" + digits

        # Landline

        if len(digits) == 11 and digits.startswith("0"):

            return digits

        return None

    # =====================================================
    # VALIDATE
    # =====================================================

    def is_valid_phone(self, phone):

        if not phone:

            return False

        digits = re.sub(r"\D", "", phone)

        if len(set(digits)) == 1:

            return False

        if phone.startswith("+91"):

            return digits[-10] in "6789"

        if phone.startswith("0"):

            return 10 <= len(digits) <= 11

        return False

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, company_id, phone, phone_type="Office", is_primary=False):

        phone = self.clean_phone(phone)

        if not self.is_valid_phone(phone):

            return

        self.db.cursor.execute("""

        SELECT id

        FROM company_phones

        WHERE company_id=?
        AND phone=?

        """, (

            company_id,

            phone

        ))

        if self.db.cursor.fetchone():

            return

        self.db.cursor.execute("""

        INSERT INTO company_phones(

            company_id,
            phone,
            phone_type,
            is_primary,
            verified

        )

        VALUES(?,?,?,?,?)

        """, (

            company_id,
            phone,
            phone_type,
            1 if is_primary else 0,
            0

        ))

        self.db.conn.commit()

        print(f"      ✓ Phone Saved : {phone}")

    # =====================================================
    # READ
    # =====================================================

    def get_by_company(self, company_id):

        self.db.cursor.execute("""

        SELECT

            MIN(id) AS id,

            phone,

            phone_type,

            MAX(is_primary) AS is_primary,

            MAX(verified) AS verified

        FROM company_phones

        WHERE company_id=?

        GROUP BY phone

        ORDER BY

            is_primary DESC,

            CASE
                WHEN phone LIKE '+91%' THEN 0
                ELSE 1
            END,

            phone

        """, (

            company_id,

        ))

        return self.db.cursor.fetchall()

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, phone_id):

        self.db.cursor.execute("""

        DELETE FROM company_phones

        WHERE id=?

        """, (

            phone_id,

        ))

        self.db.conn.commit()

    # =====================================================
    # PRIMARY
    # =====================================================

    def set_primary(self, company_id, phone_id):

        self.db.cursor.execute("""

        UPDATE company_phones

        SET is_primary=0

        WHERE company_id=?

        """, (

            company_id,

        ))

        self.db.cursor.execute("""

        UPDATE company_phones

        SET is_primary=1

        WHERE id=?

        """, (

            phone_id,

        ))

        self.db.conn.commit()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.db.close()