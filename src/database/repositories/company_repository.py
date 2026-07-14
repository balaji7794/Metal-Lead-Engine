from src.database.database import Database


class CompanyRepository:

    def __init__(self):

        self.db = Database()

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, lead):

        self.db.cursor.execute(
            """
            SELECT id
            FROM companies
            WHERE google_maps_url=?
            """,
            (lead.google_maps_url,),
        )

        row = self.db.cursor.fetchone()

        if row:

            self.db.cursor.execute(
                """
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
                """,
                (
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
                    lead.google_maps_url,
                ),
            )

            self.db.conn.commit()

            return row["id"], False

        self.db.cursor.execute(
            """
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
            """,
            (
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
                lead.notes,
            ),
        )

        self.db.conn.commit()

        return self.db.cursor.lastrowid, True

    # =====================================================
    # DASHBOARD
    # =====================================================

    def total_companies(self):

        self.db.cursor.execute("SELECT COUNT(*) FROM companies")

        return self.db.cursor.fetchone()[0]
    
    def dashboard_stats(self):

        stats = {}

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM companies WHERE website IS NOT NULL AND website<>''"
        )
        stats["websites"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM company_emails"
        )
        stats["emails"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM company_phones"
        )
        stats["phones"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM companies WHERE lead_status='New'"
        )
        stats["new"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM companies WHERE lead_status='Interested'"
        )
        stats["interested"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM companies WHERE lead_status='Follow Up'"
        )
        stats["followup"] = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM companies WHERE lead_status='Closed'"
        )
        stats["closed"] = self.db.cursor.fetchone()[0]

        return stats

    # =====================================================
    # COMPANY LIST
    # =====================================================

    def get_all(self, sort="newest"):

        order_by = {

        "newest": "id DESC",
        "oldest": "id ASC",
        "az": "company_name COLLATE NOCASE ASC",
        "za": "company_name COLLATE NOCASE DESC",
        "rating": "rating DESC, reviews DESC",
        "reviews": "reviews DESC"

        }.get(sort, "id DESC")

        self.db.cursor.execute(f"""

        SELECT *

        FROM companies

        ORDER BY {order_by}

        """)

        return self.db.cursor.fetchall()

    # =====================================================
    # SEARCH
    # =====================================================

    def search(self, keyword, sort="newest"):

        keyword = f"%{keyword}%"

        order_by = {

        "newest": "id DESC",
        "oldest": "id ASC",
        "az": "company_name COLLATE NOCASE ASC",
        "za": "company_name COLLATE NOCASE DESC",
        "rating": "rating DESC, reviews DESC",
        "reviews": "reviews DESC"

        }.get(sort, "id DESC")

        self.db.cursor.execute(f"""

        SELECT *

        FROM companies

        WHERE

            company_name LIKE ?

            OR city LIKE ?

            OR state LIKE ?

            OR category LIKE ?

        ORDER BY {order_by}

        """, (

        keyword,

        keyword,

        keyword,

        keyword

        ))

        return self.db.cursor.fetchall()

    # =====================================================
    # COMPANY DETAILS
    # =====================================================

    def get_by_id(self, company_id):

        self.db.cursor.execute(
            """
            SELECT *
            FROM companies
            WHERE id=?
            """,
            (company_id,),
        )

        return self.db.cursor.fetchone()

    # =====================================================
    # CRM
    # =====================================================

    def update_crm(
        self,
        company_id,
        lead_status,
        priority,
        last_contacted,
        next_followup,
        remarks,
    ):

        self.db.cursor.execute(
            """
            UPDATE companies
            SET
                lead_status=?,
                priority=?,
                last_contacted=?,
                next_followup=?,
                remarks=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,
            (
                lead_status,
                priority,
                last_contacted,
                next_followup,
                remarks,
                company_id,
            ),
        )

        self.db.conn.commit()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.db.close()