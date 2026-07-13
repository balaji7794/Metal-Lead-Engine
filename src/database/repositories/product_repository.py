from src.database.database import Database


class ProductRepository:

    def __init__(self):

        self.db = Database()

    def save(

        self,

        company_id,

        product_name,

        product_category="",

        grade="",

        confidence=100

    ):

        if not product_name:

            return

        product_name = product_name.strip()

        grade = grade.strip()

        self.db.cursor.execute("""

        SELECT id

        FROM company_products

        WHERE company_id=?

        AND LOWER(product_name)=LOWER(?)
        AND LOWER(IFNULL(grade,''))=LOWER(?)

        """, (

            company_id,

            product_name,

            grade

        ))

        if self.db.cursor.fetchone():

            return

        self.db.cursor.execute("""

        INSERT INTO company_products(

            company_id,

            product_name,

            product_category,

            grade,

            confidence

        )

        VALUES(?,?,?,?,?)

        """, (

            company_id,

            product_name,

            product_category,

            grade,

            confidence

        ))

        self.db.conn.commit()

        print(

            f"      ✓ {product_name}"

            + (f" [{grade}]" if grade else "")

            + (f" ({product_category})" if product_category else "")

        )

    def close(self):

        self.db.close()