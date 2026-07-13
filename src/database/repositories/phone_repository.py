from src.database.database import Database
import re


class PhoneRepository:

    def __init__(self):

        self.db = Database()

    def clean_phone(self, phone):

        if not phone:
            return None

        digits = re.sub(r"\D", "", phone)

        # -------------------------
        # Convert to +91XXXXXXXXXX
        # -------------------------

        if len(digits) == 10:

            if digits[0] in "6789":

                return "+91" + digits

            return None

        if len(digits) == 12 and digits.startswith("91"):

            return "+" + digits

        # -------------------------
        # Keep Landline
        # -------------------------

        if len(digits) == 11 and digits.startswith("0"):

            return digits

        return None

    def is_valid_phone(self, phone):

        if not phone:
            return False

        digits = re.sub(r"\D", "", phone)

        # -------------------------
        # Reject repeated digits
        # -------------------------

        if len(set(digits)) == 1:
            return False

        # -------------------------
        # Mobile
        # -------------------------

        if phone.startswith("+91"):

            mobile = digits[-10:]

            if mobile[0] not in "6789":
                return False

            return True

        # -------------------------
        # Landline
        # -------------------------

        if phone.startswith("0"):

            if len(digits) < 10 or len(digits) > 11:
                return False

            return True

        return False

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

    def close(self):

        self.db.close()