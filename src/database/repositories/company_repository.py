from src.database.database import Database


class CompanyRepository:

    def __init__(self):

        self.db = Database()

    def save(self, lead):

        self.db.cursor.execute("""

        SELECT id

        FROM companies

        WHERE google_maps_url=?

        """, (lead.google_maps_url,))

        row = self.db.cursor.fetchone()

        if row:

            self.db.cursor.execute("""

            UPDATE companies

            SET

                company_name=?,
                website=?,
                phone=?,
                email=?,
                address=?,
                city=?,
                state=?,
                country=?,
                category=?,
                rating=?,
                reviews=?,
                source=?,
                notes=?,
                updated_at=CURRENT_TIMESTAMP

            WHERE google_maps_url=?

            """, (

                lead.name,
                lead.website,
                lead.phone,
                ",".join(lead.emails),
                lead.address,
                lead.city,
                lead.state,
                lead.country,
                lead.category,
                lead.rating,
                lead.review_count,
                lead.source,
                lead.notes,
                lead.google_maps_url

            ))

            self.db.conn.commit()

            return row["id"], False

        self.db.cursor.execute("""

        INSERT INTO companies(

            company_name,
            google_maps_url,
            website,
            phone,
            email,
            address,
            city,
            state,
            country,
            category,
            rating,
            reviews,
            source,
            notes

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            lead.name,
            lead.google_maps_url,
            lead.website,
            lead.phone,
            ",".join(lead.emails),
            lead.address,
            lead.city,
            lead.state,
            lead.country,
            lead.category,
            lead.rating,
            lead.review_count,
            lead.source,
            lead.notes

        ))

        self.db.conn.commit()

        company_id = self.db.cursor.lastrowid

        return company_id, True

    def close(self):

        self.db.close()