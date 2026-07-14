from pathlib import Path
import sqlite3


class Migration:

    def __init__(self):

        Path("database").mkdir(exist_ok=True)

        self.conn = sqlite3.connect("database/metal_leads.db")

    def run(self):

        migration_folder = Path("database/migrations")

        sql_files = sorted(migration_folder.glob("*.sql"))

        cursor = self.conn.cursor()

        for sql_file in sql_files:

            try:

                print(f"Running Migration : {sql_file.name}")

                sql = sql_file.read_text(encoding="utf-8")

                cursor.executescript(sql)

                self.conn.commit()

            except sqlite3.OperationalError as e:

                if "duplicate column name" in str(e).lower():

                    print(f"Skipping : {sql_file.name}")

                    continue

                raise

        print("\n✅ Database Ready")

    def close(self):

        self.conn.close()