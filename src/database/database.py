import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/metal_leads.db")

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS companies(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company_name TEXT,

            google_maps_url TEXT UNIQUE,

            website TEXT,

            phone TEXT,

            email TEXT,

            address TEXT,

            city TEXT,

            state TEXT,

            country TEXT,

            category TEXT,

            business_type TEXT,

            products TEXT,

            scrap_generated TEXT,

            estimated_consumption_mt REAL,

            estimated_scrap_mt REAL,

            msme_type TEXT,

            rating REAL,

            reviews INTEGER,

            source TEXT,

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.conn.commit()

    def company_exists(self, maps_url):

        self.cursor.execute(

            "SELECT id FROM companies WHERE google_maps_url=?",

            (maps_url,)

        )

        return self.cursor.fetchone()

    def insert_company(self, lead):

        self.cursor.execute("""

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

        """,(

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

        self.conn.commit()

    def update_company(self, lead):

        self.cursor.execute("""

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

        """,(

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

        self.conn.commit()

    def save_company(self, lead):

        if self.company_exists(lead.google_maps_url):

            self.update_company(lead)

        else:

            self.insert_company(lead)

    def close(self):

        self.conn.close()